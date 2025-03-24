from file_database import FileDatabase
from crawler import FileCrawler

import time

def indexFiles():
    startTime = time.time()

    crawler = FileCrawler()
    db = FileDatabase()

    for fileData in crawler.crawl():
        if fileData:
            db.insertFile(fileData)
    
    endTime = time.time()
    runTime = endTime - startTime
    print(f"Indexing complete in {runTime:.2f} seconds")

indexFiles()
