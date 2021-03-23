from ..Configs import ConfigObj

import re


class StataCommon:
    def __init__(self, raw_table, config_keys, body_header_index=0):
        """

        :param raw_table:
        :param config_keys:
        :type config_keys: ConfigObj
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

        self.phenotype, self.variables, self.body = self._extract_body(body_header_index)

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

    def _extract_body(self, skip_lines=0):
        """
        This extracts the body of the table by looking for the stata dividers and then parsing out the unique elements.
        Use the first element of the first line as the phenotype, and then return the rest as column headers will be set
        based on table type.

        :return: The rows from the body as if it where a csv row
        :rtype: list
        """
        # Isolate lines with table lines within them
        table_elements = [index for index, line in enumerate(self._raw_table) if "|" in line]

        # Isolate these lines, minus the headers, without the table line elements
        body_lines = []
        for index, line in enumerate(self._raw_table):
            if min(table_elements) + skip_lines <= index and index in table_elements:
                body_lines.append([value for value in line if value != "|"])

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
