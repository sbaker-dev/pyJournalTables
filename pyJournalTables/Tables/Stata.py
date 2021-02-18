from pyJournalTables.Tables.TableObj import TableObj
from pyJournalTables.Configs.ConfigObj import ConfigObj

from pathlib import Path
import re


class StataTable(TableObj):
    def __init__(self, table_lines, table_type, key_override=None):
        """

        :param table_lines: The lines for a given table, parsed from a .log file
        :type table_lines: list

        :param key_override: If the user has an alternative set of keys in a yaml file then this can be passed here,
            else None
        :type key_override: None | str

        Attribute descriptions with * from https://stats.idre.ucla.edu/stata/output/regression-analysis/

        Attributes
        -----------
        | Observations*: The number of observations used in the regression
        | F_Stat*: The Mean Square Model divided by the Mean Square Residual yields the F stat.
        | F_Prob*: P value associate with the F Stat
        | R-Squared*: The proportion of variance in the dependent variable which be predicted from independent variables
        | Adj-R-Squared*: R squared adjusted for the number of independent variables
        | Root MSE*: The standard deviation of the error term
        | Adjusted Clusters: The number of clusters the standard error was adjusted by

        # todo set the other attributes

        """
        super().__init__(table_lines)

        # Set the string keys for extraction of values
        self.keys = self._set_keys(key_override)

        # Set the stata headers
        self.observations = self._set_stata_headers(self.keys.key_obs, int)
        self.f_stat = self._set_stata_headers(self.keys.key_f_stat)
        self.f_prob = self._set_stata_headers(self.keys.key_f_prob)
        self.r_sq = self._set_stata_headers(self.keys.key_r_sqr)
        self.adj_r_sqr = self._set_stata_headers(self.keys.key_adj_r_sqr)
        self.within_r_sqr = self._set_stata_headers(self.keys.key_within_r_sqr)
        self.root_mse = self._set_stata_headers(self.keys.key_root_mse)
        self.adjusted_clusters = self._set_stata_headers(self.keys.key_adjusted_clusters, int, True)

        # Extract the phenotype name, the variable names, the body, and set the table type
        self.phenotype, self.variables, self._body = self._extract_body()
        self._body_headers = self._set_body_headers(table_type)

        # Set all the table bodies attributes
        [setattr(self, header, [line[i] for line in self._body]) for i, header in enumerate(self._body_headers)]

    def __repr__(self):
        return f"{self.phenotype} = {' + '.join(v for v in self.variables)}"

    @staticmethod
    def _set_keys(key_override):
        """
        Keys for extracting values for certain programs contain defaults, but these can be over-written by providing a
        yaml file of custom keys

        :param key_override: Path to a yaml file or None
        :type key_override: Path | str | None

        :return: ConfigObj of the loaded dict from the yaml file
        :rtype: ConfigObj
        """
        if key_override:
            override_path = Path(key_override)
            assert override_path.exists(), "Path to yaml file to override keys used for setting attributes is not valid"
            assert override_path.suffix == ".yaml", "Yaml file invalid or does not contain the .yaml suffix"
            return ConfigObj(key_override)
        else:
            return ConfigObj(Path(Path(__file__).parent.parent, "Configs", "Stata.yaml"))

    def _set_stata_headers(self, key, return_type=float, optional=False):
        """
        Set an attribute the value header above the stata table body surrounded by ---

        :param key: The Key value to match this line to the attribute
        :type key: str

        :return: The return type of the header, by default a float but can also be an int

        :param optional: If the attribute is optional then no KeyError will be raise if the attribute is not found,
            defaults to False
        :type optional: bool

        :return:

        :raises KeyError: If the key was found but no numerical value was set, or if the key was not found.
        """
        for line in self.raw_table:
            # If we find the key in the line, extract the value from it
            if key in line:
                # Extract the numerical values from the line
                values = self._extract_values(line)

                # If we don't find any numbers but did find the observation raise an exception
                if len(values) == 0:
                    raise KeyError(f"{key} was found but no numerical value exists in line")

                # If only one value is found, return the int of that value
                elif len(values) == 1:
                    return return_type(values[0])

                # If multiple are found, given obs are on the far right, return the last value as an int
                else:
                    return return_type(values[-1])

        # If this parameter is optional, and we did not find anything in our extraction, then return None
        if optional:
            return None
        # Otherwise raise a KeyError
        else:
            raise KeyError(f"{key} was not found yet is set to be required")

    @staticmethod
    def _extract_values(line):
        """Extract numerical values from a line"""
        # Remove anything that isn't a number
        values_list = [re.sub(r"\D", "", line) for line in line.split(" ")]

        # Remove empty values
        values_list = [value for value in values_list if value != ""]

        # Restore floats
        return [value if value[0] != "0" else f"0.{value[1:]}" for value in values_list]

    def _extract_body(self):
        """
        This extracts the body of the table by looking for the stata dividers and then parsing out the unique elements.
        Use the first element of the first line as the phenotype, and then return the rest as column headers will be set
        based on table type.

        :return: The rows from the body as if it where a csv row
        :rtype: list
        """
        # Isolate lines with separators on them
        separators = [index for index, line in enumerate(self.raw_table) if "---" in line]

        body_lines = []
        for index, line in enumerate(self.raw_table):

            # We then extract lines between the start and end of the separators
            # NOTE: Stata has 'Robust' for Robust standard errors on a separate line, so we want the min + 1
            if min(separators) + 1 < index < max(separators) and index not in separators:
                # Isolate each element by splitting on spaces, keep elements that are not empty.
                parts = [part for part in line.split(" ") if part != ""]

                # The first column is a divider, so we remove it
                body_lines.append([part for i, part in enumerate(parts) if i != 1])

        # Extract the variable names, with the first one always being the phenotype/outcome
        variable_names = [line[0] for line in body_lines]
        phenotype = variable_names[0]
        variable_names = variable_names[1:]

        # Clean the body of new line expressions and convert the strings to floats
        cleaned_lines = [[self._clean_value(value) for value in line] for line in [line[1:] for line in body_lines[1:]]]

        # Return the phenotype, the variable names, and the body statistics
        return phenotype, variable_names, cleaned_lines

    def _set_body_headers(self, table_type):
        """Set the type of headers to use"""
        if table_type == "GLS":
            return self.keys.key_gls
        else:
            raise NotImplementedError("Sorry, only GLS is currently support")

    @staticmethod
    def _clean_value(value):
        """
        Clean the value of any newline expressions and then convert it to a float

        :param value: A string representation of a value from the body of the table
        :type value: str

        :return: A float representation of a value from the body of the table
        :rtype: float

        :raises ValueError: If converting to float is not possible
        """
        # Remove new line expressions
        value = re.sub("\n", "", value)

        # Negative zero starting floats without a zero will not convert
        if value[0:2] == "-.":
            return float(f"-0.{value[2:]}")
        else:
            try:
                return float(value)
            except ValueError:
                raise ValueError(f"Could not clean {value}")


def stata_table_parser(stata_log_file, table_type, table_start_key="Number of obs", divider_limit=3):
    """
    This is the importer that the user will provide the path to that will extract each table in log by iterating though
    it and using divider counts (lines of ---) to split the tables from the log

    :param stata_log_file: Path to the stata log file, must be valid and have the extension .log
    :type stata_log_file: str | Path

    :param table_type: The type regression output you are using. Takes one of the flowing case sensitive values:
        [GLS]
    :type table_type: str

    :param table_start_key: The start string that is found within a line that represents the start of a new table,
        defaults to "Number of obs"
    :type table_start_key: str

    :param divider_limit: The count of lines containing --- after the start line that represents the end of the table.
        Defaults to 3.
    :type divider_limit: int

    :return: A list StataTable objects
    :rtype: list[StataTable]
    """

    # Set the path, validate it exists, and is of the right type
    log_path = Path(stata_log_file)
    assert log_path.exists(), "Path to .log is invalid"
    assert log_path.suffix == ".log", "File is not a log as it lacks a .log file extension"

    # Initialise the holder for each table object
    tables = []

    # Iterate over the lines in the file provided
    with open(log_path) as file_to_iterate:

        start_index = 0
        divider_count = 0
        set_tables = []
        for index, line in enumerate(file_to_iterate):

            # If the number of obs is in the line, then reset the dividers count and set the start index
            if table_start_key in line:
                divider_count = 0
                start_index = index

            # If a divider is found, iterate up the divider count
            if "---" in line:
                divider_count += 1

            # If the number of dividers found since the start index equals the limit, create a table object
            if divider_count == divider_limit and start_index not in set_tables:

                # Extract the lines between the start index and the current index for the object
                with open(log_path) as extractor:
                    table_lines = [table_line for i, table_line in enumerate(extractor) if start_index <= i <= index]

                # Append the object to the tables list and the current index to the set table indexes.
                tables.append(StataTable(table_lines, table_type))
                set_tables.append(start_index)

    return tables
