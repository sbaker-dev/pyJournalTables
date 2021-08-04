from stataLogObject.Configs.ConfigObj import TableConfigs, Table
from stataLogObject.StataParser import StataRaw
from stataLogObject.StataParser.StataTable import StataTable

from pathlib import Path


class StataLog:
    def __init__(self, log_path):

        # Set the log path, validate it exists, and that it is .log
        self.log_path = Path(log_path)
        assert self.log_path.exists(), "Path to .log is invalid"
        assert self.log_path.suffix == ".log", "File is not a log, as it lacks a .log file extension"

        # Set the config object for known table types
        self.config = TableConfigs()

        # Create lists of table objects for each object in the self.config
        self.ols = self.create_tables(self.config.ols)
        self.ols_clu = self.create_tables(self.config.ols_clu)
        self.hdfe = self.create_tables(self.config.hdfe)

        self.summary = self.create_tables(self.config.summary)

    def create_tables(self, config):
        """
        For a Given configuration, isolate the raw table then format it to StataTable Generic

        :param config: The configuration Table Object for this log table that we wish to isolate
        :type config: Table
        """
        return [StataTable(table, config) for table in StataRaw(self.log_path, config.table_ext).raw_tables]



#
a = StataLog(r"C:\Users\Samuel\PycharmProjects\stataLogObject\DoLogs\StataLog.log")

b = a.summary[0]

print(b.table_columns)

def forest_plot(table, exclusions=None):
    """

    :param table:
    :type table: StataTable
    :param exclusions:
    :return:
    """

    if exclusions is None:
        row_indexes = [i for i, _ in enumerate(table.var_names)]
    else:
        row_indexes = [i for i, var in enumerate(table.var_names) if var not in exclusions]

    # Isolate each rows values
    output = []
    for index, (var, coef, lb, ub) in enumerate(zip(table.var_names, table.coefficients, table.lb_95, table.ub_95)):
        if index in row_indexes:
            output.append([var, coef, lb, ub])

    print(output)

# forest_plot(b, ['_cons'])