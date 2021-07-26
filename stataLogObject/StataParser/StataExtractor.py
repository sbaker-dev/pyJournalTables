from stataLogObject.StataParser.StataCommon import StataCommon
from stataLogObject.Tables import *
from stataLogObject.Configs import ConfigObj

from pathlib import Path
import re


class StataExtractor:
    def __init__(self, log_path, key_override=None):

        # Check the file is a log file
        self.log_path = Path(log_path)
        assert self.log_path.exists(), "Path to .log is invalid"
        assert self.log_path.suffix == ".log", "File is not a log, as it lacks a .log file extension"

        # Set the config args
        self._config = self._set_keys(key_override)

        # Extract known tables from the log file
        self._ols_raw = self._extract_raw(self._config.key_ols_divider, 1, skip_indexes=[9])
        self._hdfe_raw = self._extract_raw(self._config.key_hdfe_divider, 1, skip_indexes=[7])
        self._summary_raw = self._extract_raw(self._config.key_sum_divider)
        self._tab_raw = self._extract_raw(self._config.key_tab_divider, skip_indexes=[0])
        self._fe_raw = self._extract_raw(self._config.key_fe_within_divider, 3, skip_indexes=[7])

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

    def _extract_raw(self, isolate_key, space_count=0, skip_indexes=None):
        """
        This uses an isolate_key to group lines, represented as a list of space limited elements, from a log file

        This uses the isolate_key, itself a list of space limited elements, to check against a line found in a space
        limited element in the log file. If the element needed to be extract contains elements that may be unique per
        table, for example in tab the first element is the var name, these can be removed via skip_indexes

        Once found we can then isolate individual elements by grouping lines between empty lines, where the number of
        empty lines allowed is set via space_count.

        :param isolate_key: A list of space limited strings to be found in the log file that represents the start.
        :type isolate_key: list[str]

        :param skip_indexes: If the raw list of elements found in the log needs to have certain elements skipped, then
            provide a list of ints to to skip_indexes
        :type skip_indexes: list[int]

        :param space_count: The number of spaces allowed before the table is considered finished and is saved, defaults
            to 1
        :type space_count: int

        :return: A list of the raw lines, grouped into tables, that can then be used to isolate the table elements
        :rtype: list[list[list[str]]]
        """

        # Set the return list
        total_elements_found = []

        # If no indexes are to be set, then set skip_indexes to be empty
        if skip_indexes is None:
            skip_indexes = []

        # Set the per table iterable elements
        current_element = []
        spacer = 0
        start_index = None

        with open(self.log_path, "r") as log_file:

            for index, line in enumerate(log_file):
                # Convert the string line with regular expressions into a list of space separated items.
                cleaned = self._clean_line(line)

                # If the cleaned line, minus any skip_indexes, matches our isolate_key
                if [v for i, v in enumerate(cleaned) if i not in skip_indexes] == isolate_key:
                    # Then reset our elements and set the start index
                    current_element = []
                    start_index = index
                    spacer = 0

                # If we find an empty line, and we have reached the limited of empty lines we are allowed to find
                if len(cleaned) == 0 and spacer == space_count:
                    # If we have isolated something which contains elements, add it to the return list of tables
                    if len(current_element) > 0:
                        total_elements_found.append(current_element)

                    # Reset the table specific elements
                    current_element = []
                    start_index = None
                    spacer = 0

                # Otherwise if the line is empty but less than the allowed maximum, iterate the found empty upwards
                elif len(cleaned) == 0 and spacer < space_count:
                    spacer += 1

                # If we are currently within a table and the length of cleaned != 0, then append to current_element
                elif start_index:
                    current_element.append(cleaned)

        return total_elements_found

    @staticmethod
    def _clean_line(line):
        """
        Strip line of new line element then return, replacing negative floats without a 0, -.{value} with -0.{value}

        :param line: Line in the log file
        :type line: str
        """
        subbed = "".join([re.sub("\n", "", value) for value in line])
        return [f"-0.{v[2:]}" if v[0:2] == "-." else v for v in subbed.split(" ") if len(v) > 0]

    def censure_log(self):
        """
        Logs from stata often contain a path which can be problematic if they are to sensitive locations so this
        censures them.

        :return: Nothing, override the log file
        :rtype: None
        """

        # Remove the path to log: locations
        log_raw = []
        with open(self.log_path, "r") as log_file:
            for line in log_file:
                if "log:" in line:
                    log_raw.append(f"{line.split(':')[0]}: \n")
                else:
                    log_raw.append(line)

        # Override the file
        with open(self.log_path, "w") as log_file:
            for line in log_raw:
                log_file.write(line)

    @property
    def ols_tables(self):
        """
        Return the OLS tables for this log

        :return: A list of OLS table objects
        :type: list[OLS]
        """
        return [OLS(StataCommon(table, self._config, skip_indexes=[0, 1, 2, 3, 4, 5])) for table in self._ols_raw]

    @property
    def hdfe_tables(self):
        """
        Return the HDFE tables, created by reghdfe https://scorreia.com/software/reghdfe/index.html , for this log

        :return: A list of HDFE table objects
        :type: list[HDFE]
        """
        return [HDFE(StataCommon(table, self._config, 1)) for table in self._hdfe_raw]

    @property
    def fe_tables(self):
        """
        Returns the Fixed effects within regression tables
        :return: list[FEWithin]
        """
        return [FEWithin(StataCommon(table, self._config, skip_indexes=[-1, -2, -3])) for table in self._fe_raw]

    @property
    def sum_tables(self):
        """
        Returns the Summary Stats tables for this log

        :return: A list of SummaryStats
        :rtype: list[SummaryStats]
        """
        return [SummaryStats(StataCommon(table, self._config)) for table in self._summary_raw]

    @property
    def tab_tables(self):
        """
        Returns the tabulated tables for this log

        :return: A list of Tabulate
        :rtype: list[Tabulate]
        """
        return [Tabulate(StataCommon(table, self._config)) for table in self._tab_raw]
