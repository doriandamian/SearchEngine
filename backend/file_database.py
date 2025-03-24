import sqlite3

class FileDatabase:
    def __init__(self, dbName = "database.db"):
        self.conn = sqlite3.connect("../database/" + dbName, check_same_thread=False)

    def insertFile(self, fileData):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO files (path, title, extension, content, created_at, modified_at, size)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', fileData)
        self.conn.commit()

    def searchFiles(self, query):
        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT f.path, f.title, f.extension, f.content, f.created_at, f.modified_at, f.size
        FROM files AS f
        INNER JOIN files_fts AS fts
        ON f.id = fts.id
        WHERE fts.title LIKE ? OR fts.content LIKE ?
        ORDER BY bm25(files_fts)
        LIMIT 20;
        """, (f"%{query}%", f"%{query}%"))

        results = cursor.fetchall()
        return results