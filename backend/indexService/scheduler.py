from logger import Logger

from backend.file_database import FileDatabase
from crawler import FileCrawler

def indexFiles():
    crawler = FileCrawler()
    db = FileDatabase()
    logger = Logger()
    fileCount = 0

    for fileData in crawler.crawl(logger):
        if fileData:
            db.insertFile(fileData)
            fileCount += 1

    logger.addLog(f"All files indexed succesfully.")
    logger.finish(fileCount)

indexFiles()