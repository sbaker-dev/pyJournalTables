from stataLogObject.Configs.ConfigObj import TableConfigs, Table
from stataLogObject.StataParser import StataRaw
from stataLogObject.StataParser.StataTable import StataTable

from pathlib import Path


class StataLog:
    def __init__(self, log_path):

        # TODO Error handle non .logs

        self.log_path = Path(log_path)
        self.config = TableConfigs()

        # Create lists of table objects
        self.ols = self.create_tables(self.config.ols)
        self.ols_clu = self.create_tables(self.config.ols_clu)
        self.hdfe = self.create_tables(self.config.hdfe)

    def create_tables(self, config):
        """
        For a Given configuration, isolate the raw table then format it to StataTable Generic

        :param config: The configuration Table Object for this log table that we wish to isolate
        :type config: Table
        """
        return [StataTable(table, config) for table in StataRaw(self.log_path, config.table_ext).raw_tables]


StataLog(r"C:\Users\Samuel\PycharmProjects\stataLogObject\DoLogs\MultiTableLog.log")
