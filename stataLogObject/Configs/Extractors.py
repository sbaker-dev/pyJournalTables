from stataLogObject.Configs.TableEntries import Entry
from dataclasses import dataclass, field
from typing import List


# TODO: Make Generalised Extract given common elements of separator/Skip lines and skip indexes?
@dataclass
class ExtractBody:
    body_type: Entry
    skip_lines: int = 0
    skip_indexes: List = field(default_factory=lambda: [])

    def format_indexes(self, table_length):
        """
        We may need to subtract indexes from the bottom, in which case the index is relative to the table length

        Note
        ----
        Table length is not base zero, hence why we need to take one way from it
        negative skip indexes are formatted in the same way as indexing, so -1 retrieves the last element. However, if
            we take the index of -1 from the table length then we always skip the second to last element. We can't use
            zero, as zero is an actual index for the first element. As such, each negative value gets +1 added to it.
        """
        self.skip_indexes = [v if v >= 0 else (table_length - 1) + (v + 1) for v in self.skip_indexes]


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