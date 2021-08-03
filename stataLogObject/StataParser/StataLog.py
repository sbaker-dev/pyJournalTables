from stataLogObject.Configs.ConfigObj import TableConfigs
from stataLogObject.StataParser import StataRaw
from stataLogObject.StataParser.StataTable import StataTable

from pathlib import Path


class StataLog:
    def __init__(self, log_path):

        # TODO Error handle non .logs

        self.log_path = Path(log_path)
        self.config = TableConfigs()

        self.raw_ols = [StataTable(table, self.config.ols)
                        for table in StataRaw(self.log_path, self.config.ols.table_ext).raw_tables]

        for t in self.raw_ols:
            print(t.p_z_value)


StataLog(r"C:\Users\Samuel\PycharmProjects\stataLogObject\DoLogs\MultiTableLog.log")
