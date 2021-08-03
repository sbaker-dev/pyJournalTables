from pathlib import Path
import re


class StataRaw:
    def __init__(self, log_path, divider, space_count, skip_indexes=None):
        """

        :param log_path: The path to the log file
        :type log_path: Path

        :param divider: The divider to isolate the elements
        :type divider: list[str]

        :param space_count: The number of spaces allowed before the table is considered finished and is saved
        :type space_count: int

        :param skip_indexes: Option list of elements found in the log needs to have certain elements skipped
        :type skip_indexes: None | list[int]
        """

        # Initializers
        self._log_path = log_path
        self.divider = divider
        self.space_count = space_count
        if skip_indexes is None:
            self.skip_indexes = []
        else:
            self.skip_indexes = skip_indexes

        # Raw table that has been extracted
        self.raw_tables = [self._extract_raw_table(i) for i in self._find_start_indexes()]

    def _find_start_indexes(self):
        """
        Find the starting indexes
        :return:
        """

        start_indexes = []
        with open(self._log_path, "r") as log_file:
            for index, line in enumerate(log_file):
                # If the cleaned line, minus any skip_indexes, matches our isolate_key
                if [v for i, v in enumerate(self._clean_line(line)) if i not in self.skip_indexes] == self.divider:

                    # Append the index - 1, as we don't want to skip this line we want to start with it
                    start_indexes.append(index)

        return start_indexes

    def _extract_raw_table(self, index):
        """
        For each given start index, isolate the elements of this table given the space_count

        :param index: The current start index of the file lines
        :type index: int

        :return: The list of all the rows that are relevant to this table
        :rtype: list
        """
        # Set the per table iterable elements
        current_element = []
        spacer = 0

        with open(self._log_path, "r") as log_file:

            # Skip the lines we don't need for this table index
            [log_file.readline() for _ in range(index)]

            for index, line in enumerate(log_file):
                # Convert the string line with regular expressions into a list of space separated items.
                cleaned = self._clean_line(line)

                # If we find an empty line, and we have reached the limited of empty lines we are allowed to find
                if (len(cleaned) == 0) and (spacer == self.space_count) and (len(current_element) > 0):
                    return current_element

                # Otherwise if the line is empty but less than the allowed maximum, iterate the found empty upwards
                elif len(cleaned) == 0 and spacer < self.space_count:
                    spacer += 1

                # If we are currently within a table then append to current_element
                else:
                    current_element.append(cleaned)

        return current_element

    @staticmethod
    def _clean_line(line):
        """
        Strip line of new line element then return, replacing negative floats without a 0, -.{value} with -0.{value}

        :param line: Line in the log file
        :type line: str
        """
        subbed = "".join([re.sub("\n", "", value) for value in line])
        return [f"-0.{v[2:]}" if v[0:2] == "-." else v for v in subbed.split(" ") if len(v) > 0]


