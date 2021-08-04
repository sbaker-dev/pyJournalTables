from stataLogObject.Configs.ConfigObj import MFVar, Table
from stataLogObject.Supports.supports import extract_values, clean_value
from stataLogObject.Supports.Errors import HeaderKeyExtractError, InvalidKeyExtract


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

        # For the body isolate, create reference and format the indexes relative to the length of the table
        self.iso = self.config.body_iso
        self.iso.format_indexes(len(self._raw))

        # Set the supporting table header values
        self.model_fit_names = self.config.mf.field_names()

        [setattr(self, f, self._set_mf(f)) for f in self.model_fit_names]
        self.model_fit = {f: getattr(self, f) for f in self.model_fit_names if getattr(self, f) is not None}

        # Extract phenotype, variable names, and the table body in row form
        self.table_col_names = self.iso.body_type.entry_names
        self.phenotype, self.body_values = self._extract_body()

        # Set the column data format
        [setattr(self, f"tb_{field}", [getattr(v, field) for v in self.body_values])for field in self.table_col_names]
        self.table_columns = {field: getattr(self, f"tb_{field}") for field in self.table_col_names}

    def _set_mf(self, f):
        """Set a given model fit parameter if it has been set, else return None as this variable was optional"""
        if not getattr(self.config.mf, f):
            return None
        else:
            return getattr(self.config.mf, f).find_mf(self._raw, f)

    def _extract_body(self):
        """
        This extracts the body of the table by looking for the stata dividers and then parsing out the unique elements.
        Use the first element of the first line as the phenotype, and then return the rest as column headers will be set
        based on table type.

        :return: A str of the phenotype and a list of TableEntry
        :rtype: (str, list[TableEntry])
        """

        # Isolate results with tables based on table line delimiters, skip indexes in the skip_indexes if provided
        result_indexes = [i for i, line in enumerate(self._raw) if ("|" in line) and (i not in self.iso.skip_indexes)]

        # Isolate these lines without the table line elements
        body_lines = self._extract_body_lines(result_indexes)

        # # Extract the variable names, with the first one always being the phenotype/outcome
        phenotype = body_lines[0][0]

        # Return the phenotype, variable names, and the table bodies formatted values
        return phenotype, self._create_table_entries(body_lines)

    def _extract_body_lines(self, result_indexes):
        """
        This will strip out the lines without the table line elements.

        :param result_indexes: The indexes of the results table
        :type result_indexes: list[int]

        :return: A list of each row that is in the table body
        :rtype: list[list[str]]
        """
        body_lines = []
        for index, line in enumerate(self._raw):
            # TODO: This feels like a very strange if statement...
            if min(result_indexes) + self.iso.skip_lines <= index and index in result_indexes:

                # Not all regression types will be without blanks, so this only adds rows that where the value is more
                # than just he name of the variable
                values_stripped = [value for value in line if value != "|"]
                if len(values_stripped) > 1:
                    body_lines.append(values_stripped)

                    # Most tables end with _cons so we can stop after this point
                    if values_stripped[0] == "_cons":
                        break
        return body_lines

    def _create_table_entries(self, body_lines):
        """Clean the values which are not the table header, create Entry of type Body_Type for each line accordingly"""
        return [self.iso.body_type.create_entry(line) for line in self._limit_var_names(body_lines)]

    def _limit_var_names(self, body_lines):
        """
        Extract the values then format them

        Note
        ----
        After extracting the values, it is possible that space seperated names may lead to more elements in a row than
        there are columns to accept them. Here after extracting the values, we format them relative to the length of
        table headers

        :param body_lines: Each line from the body that is a variable result
        :type body_lines: list[list[str]]

        :return: Formatted lines
        :rtype: list[list]
        """
        value_lines = [[clean_value(value) for value in line] for line in body_lines[1:]]
        return [line if len(line) == len(self.table_col_names) else self._line_format(line) for line in value_lines]

    def _line_format(self, line):
        """Format line relative to the number of table headers"""
        values = line[-(len(self.table_col_names) - 1):]
        var_name = "_".join(line[:-(len(self.table_col_names) - 1)])
        return [var_name] + values
