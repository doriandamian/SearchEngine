import sqlite3
import time


class FileDatabase:
    def __init__(self, dbName="database.db"):
        self.conn = sqlite3.connect("../database/" + dbName, check_same_thread=False)

    def insertFile(self, fileData):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT OR IGNORE INTO files (path, title, extension, content, created_at, modified_at, size, score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            fileData,
        )
        self.conn.commit()

    def insertSearch(self, keyword, search_type):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO searches (keyword, search_type, searched_at)
            VALUES (?, ?, ?)
            ON CONFLICT(keyword, search_type) DO UPDATE SET searched_at=excluded.searched_at
        """,
            (keyword, search_type, time.ctime()),
        )
        self.conn.commit()

    def getSearches(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT keyword, search_type FROM searches ORDER BY searched_at DESC"
        )
        results = cursor.fetchall()
        return results

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

        if wheres:
            whereString = " AND ".join(wheres)
        else:
            whereString = "1=1"

        cursor.execute(
            f"""
            SELECT f.path, f.title, f.extension, f.content, f.created_at, f.modified_at, f.size, f.score
            FROM files AS f
            INNER JOIN files_fts AS fts ON f.id = fts.id
            WHERE {whereString}
            ORDER BY score DESC
            LIMIT 20;
            """,
            params,
        )

        results = cursor.fetchall()
        return results
