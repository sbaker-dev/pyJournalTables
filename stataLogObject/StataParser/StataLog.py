from stataLogObject.Configs.ConfigObj import ConfigObj2
from stataLogObject.StataParser import StataRaw

from pathlib import Path


class StataLog:
    def __init__(self, log_path):

        self.log_path = Path(log_path)
        self.cf = ConfigObj2()

        self.raw_ols = StataRaw(self.log_path, self.cf.isolates.ols)

        print(len(self.raw_ols.raw_tables))


StataLog(r"C:\Users\Samuel\PycharmProjects\stataLogObject\DoLogs\MultiTableLog.log")