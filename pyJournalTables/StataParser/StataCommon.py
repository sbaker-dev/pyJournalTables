from ..Configs import ConfigObj

import re


class StataCommon:
    def __init__(self, raw_table, config_keys, body_header_index=0, skip_indexes=None):
        """

        :param raw_table: The lines for a given table, parsed from a .log file
        :type raw_table: list

        :param config_keys: The Configuration Object to use
        :type config_keys: ConfigObj

        :param body_header_index: Number of headers to skip in addition to the first
        :type body_header_index: int

        Attribute descriptions with * from https://stats.idre.ucla.edu/stata/output/regression-analysis/

        Attributes
        -----------
        | Observations*: The number of observations used in the regression
        | F_Stat*: The Mean Square Model divided by the Mean Square Residual yields the F stat.
        | F_Prob*: P value associate with the F Stat
        | R-Squared*: The proportion of variance in the dependent variable which be predicted from independent variables
        | Adj-R-Squared*: R squared adjusted for the number of independent variables
        | Root MSE*: The standard deviation of the error term
        | Adjusted Clusters: The number of clusters the standard error was adjusted by, optional

        # TODO do the rest of them
        """

        self._raw_table = raw_table
        self.keys = config_keys

        # Set the attributes commonly found in OLS or similar regressions, normally above the output hence 'headers'
        self.observations = self._set_stata_headers(self.keys.key_obs, int)
        self.f_stat = self._set_stata_headers(self.keys.key_f_stat)
        self.f_prob = self._set_stata_headers(self.keys.key_f_prob)
        self.r_sq = self._set_stata_headers(self.keys.key_r_sqr)
        self.adj_r_sqr = self._set_stata_headers(self.keys.key_adj_r_sqr)
        self.within_r_sqr = self._set_stata_headers(self.keys.key_within_r_sqr)
        self.root_mse = self._set_stata_headers(self.keys.key_root_mse)
        self.adjusted_clusters = self._set_stata_headers(self.keys.key_adjusted_clusters, int)

        # Initialise potential values from the body of the table
        self.coefficients = None
        self.std_errs = None
        self.t_stats = None
        self.p_stats = None
        self.conf_95_min = None
        self.conf_95_max = None

        self.phenotype, self.variables, self.body = self._extract_body(body_header_index, skip_indexes)

    def _set_stata_headers(self, key, return_type=float):
        """
        Set an attribute the value header above the stata table body surrounded by ---

        :param key: The Key value to match this line to the attribute
        :type key: str

        :return: The return type of the header, by default a float but can be converted to any type provided

        :raises KeyError: If the key was found but no numerical value was set, or if the key was not found.
        """
        for line in self._raw_table:
            # If we find the required keys in the line, extract the value from it
            if set(key).issubset(line):
                # Extract the numerical values from the line
                values = self._extract_values(" ".join([value for value in line]))

                # If we don't find any numbers but did find the observation raise an exception
                if len(values) == 0:
                    raise KeyError(f"{key} was found but no numerical value exists in line")

                elif str(key_extract).isdigit():
                    try:
                        return return_type(values[key_extract])
                    except KeyError:
                        raise KeyError(f"{key} was found but {key_extract} is out of bounds to extract from {values}")

                # If only one value is found, return the int of that value
                elif len(values) == 1:
                    return return_type(values[0])

                # If multiple are found, given obs are on the far right, return the last value as an int
                else:
                    return return_type(values[-1])

    @staticmethod
    def _extract_values(line):
        """Extract numerical values from a line"""
        # Remove anything that isn't a number
        values_list = [re.sub(r"\D", "", line) for line in line.split(" ")]

        # Remove empty values
        values_list = [value for value in values_list if value != ""]

        # Restore floats
        return [value if value[0] != "0" else f"0.{value[1:]}" for value in values_list]

    def _extract_body(self, skip_lines=0, skip_indexes=None):
        """
        This extracts the body of the table by looking for the stata dividers and then parsing out the unique elements.
        Use the first element of the first line as the phenotype, and then return the rest as column headers will be set
        based on table type.

        :param skip_lines: How many additional lines you wish to skip after the header, defaults to 0
        :type skip_lines: int

        :param skip_indexes: Indexes to ignore looking for elements, defaults to None
        :type skip_indexes: None | list[int]

        :return: The rows from the body as if it where a csv row
        :rtype: list
        """

        if skip_indexes is None:
            skip_indexes = []

        # Isolate lines with table lines within them, skip indexes in the skip_indexes if provided
        table_elements = [index for index, line in enumerate(self._raw_table)
                          if "|" in line and index not in skip_indexes]

        # Isolate these lines, minus the headers, without the table line elements
        body_lines = []
        for index, line in enumerate(self._raw_table):
            if min(table_elements) + skip_lines <= index and index in table_elements:

                # Not all regression types will be without blanks, so this only adds rows that where the value is more
                # than just he name of the variable
                values_stripped = [value for value in line if value != "|"]
                if len(values_stripped) > 1:
                    body_lines.append(values_stripped)

        # Extract the variable names, with the first one always being the phenotype/outcome
        variable_names = [line[0] for line in body_lines]
        phenotype = variable_names[0]
        variable_names = variable_names[1:]

        # Clean the body of new line expressions and convert the strings to floats
        cleaned_lines = [[self._clean_value(value) for value in line] for line in [line[1:] for line in body_lines[1:]]]

        # Return the phenotype, the variable names, and the body statistics
        return phenotype, variable_names, cleaned_lines

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

        # Change any numeric commas to periods
        value = re.sub(",", "", value)

        # Negative zero starting floats without a zero will not convert
        if value[0:2] == "-.":
            return float(f"-0.{value[2:]}")
        else:
            try:
                return float(value)
            except ValueError:
                return str(value)
