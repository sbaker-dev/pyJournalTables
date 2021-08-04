from stataLogObject.Configs.ConfigObj import Table

from miscSupports import flip_list
from csvObject import write_csv


class StataTable:
    def __init__(self, raw_table, config):
        """
        A generic Stata Table

        :param raw_table: The raw table from StataRaw object
        :type raw_table: list[list]

        :param config: The attributes of the Table to configure with
        :type config: Table

        """

        # Raw table reference and the configuration for this table
        self._raw = raw_table
        self.config = config

        # Set the supporting table header values
        self.model_fit_names = self.config.mf.field_names()

        [setattr(self, f, self._set_mf(f)) for f in self.model_fit_names]
        self.model_fit = {f: getattr(self, f) for f in self.model_fit_names if getattr(self, f) is not None}

        # Extract phenotype, variable names, and the table body in row form
        self.table_col_names = self.config.body_iso.body_type.entry_names
        self.phenotype, self.body_values = self.config.body_iso.extract_body(self._raw)

        # Set the column data format
        [setattr(self, f"tb_{field}", [getattr(v, field) for v in self.body_values])for field in self.table_col_names]
        self.table_columns = {field: getattr(self, f"tb_{field}") for field in self.table_col_names}

    def _set_mf(self, f):
        """Set a given model fit parameter if it has been set, else return None as this variable was optional"""
        if not getattr(self.config.mf, f):
            return None
        else:
            return getattr(self.config.mf, f).find_mf(self._raw, f)

    def body_to_csv(self, write_directory, write_name):
        """Write the body as a csv to the write directory called 'write_name'.csv"""
        write_csv(write_directory, write_name, list(self.table_columns.keys()), flip_list(self.table_columns.values()))
