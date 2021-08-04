from dataclasses import dataclass, field
from typing import List


# TODO: Make Generalised Extact given common elements of separator and skip indexes?
@dataclass
class ExtractBody:
    skip_lines: int = 0
    skip_indexes: List = field(default_factory=lambda: [])
    p_value: bool = True

    def format_indexes(self, table_length):
        """We may need to subtract indexes from the bottom, in which case the index is relative to explanatory variables"""

        # # TODO ???? Why is it minus 2
        # print(table_length)
        # for v in self.skip_indexes:
        #     if v < 0:
        #         print((table_length - 2) + v)

        self.skip_indexes = [v if v >= 0 else (table_length - 2) + v for v in self.skip_indexes]


@dataclass
class ExtractTable:
    """
    | Contains the information needed for extraction
    |
    | *Attributes*:
    |    **divider (list)**: The divider to isolate the elements
    |    **separator (int)**: The number of spaces allowed before the table is considered finished and is saved
    |    **skip_indexes** (Optional[list]):  Option list of elements found in the log needs to have certain elements
    |   skipped

    """
    divider: List
    separator: int
    skip_indexes: List = field(default_factory=lambda: [])