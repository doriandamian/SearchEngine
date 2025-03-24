from datetime import datetime

class Logger:
    def __init__(self):
        self.stringBuilder = f"\n\nIndexing started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n"
        self.startTime = datetime.now()

    def addLog(self, log):
        logTime = datetime.now() - self.startTime
        self.stringBuilder += f"({logTime}) [LOG] - {log}\n"

    def addError(self, msg):
        logTime = datetime.now() - self.startTime
        self.stringBuilder += f"({logTime}) [ERROR] - {msg}\n"

    def finish(self, newFiles):
        finishTime = datetime.now() - self.startTime
        self.stringBuilder += f"Indexing stopped at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Total time: {finishTime}. Total new files indexed: {newFiles}."
        with open("logs.txt", "a", encoding="utf-8") as file:
            file.write(self.stringBuilder)