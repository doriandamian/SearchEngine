import sqlite3
import time

class FileDatabase:
    def __init__(self, dbName = "database.db"):
        self.conn = sqlite3.connect("../database/" + dbName, check_same_thread=False)

    def insertFile(self, fileData):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO files (path, title, extension, content, created_at, modified_at, size, score)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        ''', fileData)
        self.conn.commit()

    def insertSearch(self, keyword):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO searches (keyword, searched_at)
            VALUES (?, ?)
            ON CONFLICT(keyword) DO UPDATE SET searched_at=excluded.searched_at
        ''', (keyword, time.ctime()))
        self.conn.commit()

    def getSearches(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT keyword FROM searches ORDER BY searched_at DESC")
        results = cursor.fetchall()
        return [row[0] for row in results]

    def searchFiles(self, query):
        cursor = self.conn.cursor()
        wheres = []
        params = []

        for key, values in query.items():
            temp = []
            for value in values:
                temp.append(f"fts.{key} LIKE ?")
                params.append(f"%{value}%")
            wheres.append(f"({' AND '.join(temp)})")
        
        # Formula:
        # Shorter path
        # More recent modified_at
        # Higher bm25
        scoreFormula = f"""
            (
                (1000.0 / LENGTH(f.path)) + 
                (strftime('%s', 'now') - strftime('%s', f.modified_at)) / -86400.0
            ) - bm25(files_fts)
        """

        if wheres:
            whereString = ' AND '.join(wheres)
        else:
            whereString = "1=1"

        cursor.execute(f"""
        SELECT f.path, f.title, f.extension, f.content, f.created_at, f.modified_at, f.size, f.score
        FROM files AS f
        INNER JOIN files_fts AS fts ON f.id = fts.id
        WHERE {whereString}
        ORDER BY score DESC
        LIMIT 20;
        """, params)

        results = cursor.fetchall()
        return results