import sqlite3

class FileDatabase:
    def __init__(self, dbName = "database.db"):
        self.conn = sqlite3.connect("../database/" + dbName)

    def insertFile(self, fileData):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO files (path, title, extension, content, created_at, modified_at, size)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', fileData)
        self.conn.commit()