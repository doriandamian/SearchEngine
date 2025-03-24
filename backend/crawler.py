import os, time

from file_database import FileDatabase

class FileCrawler:
    def __init__(self, root_dir = "/Users/doriandamian", ignoredDirs = [".git", "__pycache__"]):
        self.root_dir = root_dir
        self.ignoredDirs = ignoredDirs
        self.db = FileDatabase()
        
    def crawl(self, logger):
        cursor = self.db.conn.cursor()
        filesData = []

        for dirPath, dirNames, fileNames in os.walk(self.root_dir):
            dirNames[:] = [d for d in dirNames if d not in self.ignoredDirs]

            for file in fileNames:
                if file.endswith(".txt"):
                    filePath = os.path.join(dirPath, file)
                    stat = os.stat(filePath)

                    cursor.execute("SELECT modified_at from files where path = ? and title = ?", (dirPath, os.path.splitext(file)[0]))
                    modified_at = cursor.fetchone()

                    if modified_at:
                        if modified_at[0] == time.ctime(stat.st_ctime):
                            logger.addLog(f"File {filePath} not modified since last indexing. Skipping indexing.")
                            continue
                        else:
                            cursor.execute("DELETE FROM files WHERE path = ? AND title = ?", (dirPath, file))
                            self.db.conn.commit()
                            logger.addLog(f"File {dirPath}/{file} modified. Removing old entry from database.")

                    try:
                        with open(filePath, "r", encoding="utf-8") as f:
                            content = f.read()[:300]

                        filesData.append((
                            dirPath,                    # Path
                            os.path.splitext(file)[0],  # Title
                            os.path.splitext(file)[1],  # Extension
                            content,                    # Content
                            time.ctime(stat.st_ctime),  # Created_at
                            time.ctime(stat.st_mtime),  # Modified_at
                            stat.st_size                # Size
                        ))
                        print(dirPath, file)
                        logger.addLog(f"File {filePath} added to the indexing list.")
                    except Exception as e:
                            print(f"Error reading {filePath}: {e}")
    
        return filesData