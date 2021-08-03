from stataLogObject.Configs.ConfigObj import Extractor

from pathlib import Path
import re


class StataRaw:
    def __init__(self, log_path, isolator):
        """

        :param log_path: The path to the log file
        :type log_path: Path

        :param isolator: The Extraction elements for this table, contains dividers, space count and skip indexes
        :type isolator: Extractor
        """

        # Initializers
        self._log_path = log_path
        self.iso = isolator

        # Raw table that has been extracted
        self.raw_tables = [self._extract_raw_table(i) for i in self._find_start_indexes()]

    def _find_start_indexes(self):
        """
        Find the starting indexes from the log file where the line matches the divider
        """
        with open(self._log_path, "r") as log_file:
            return [index for index, line in enumerate(log_file) if self._evaluate_start_line(line)]

    def _evaluate_start_line(self, line):
        """Evaluate if the cleaned start line, minus elements in skip_indexes, equals the divider"""
        return [v for i, v in enumerate(self._clean_line(line)) if i not in self.iso.skip_indexes] == self.iso.divider

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
                if (len(cleaned) == 0) and (spacer == self.iso.separator) and (len(current_element) > 0):
                    return current_element

                # Otherwise if the line is empty but less than the allowed maximum, iterate the found empty upwards
                elif len(cleaned) == 0 and spacer < self.iso.separator:
                    spacer += 1

                # If we are currently within a table then append to current_element
                else:
                    current_element.append(cleaned)

        return current_element

    # TODO Extract so that it can be used for custom classes
    @staticmethod
    def _clean_line(line):
        """
        Strip line of new line element then return, replacing negative floats without a 0, -.{value} with -0.{value}

        :param line: Line in the log file
        :type line: str
        """
        subbed = "".join([re.sub("\n", "", value) for value in line])
        return [f"-0.{v[2:]}" if v[0:2] == "-." else v for v in subbed.split(" ") if len(v) > 0]
