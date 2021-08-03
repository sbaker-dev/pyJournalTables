from miscSupports import parse_as_numeric
from string import ascii_letters
import re


def clean_line(line):
    """
    Strip line of new line element then return, replacing negative floats without a 0, -.{value} with -0.{value}

    :param line: Line in the log file
    :type line: str
    """
    subbed = "".join([re.sub("\n", "", value) for value in line])
    return [f"-0.{v[2:]}" if v[0:2] == "-." else v for v in subbed.split(" ") if len(v) > 0]


def extract_values(line):
    """Extract numerical values from a line"""

    values = [split_line.strip(ascii_letters).replace(",", "") for split_line in line.split()]

    values_return = []
    for v in values:
        try:
            values_return.append(float(v))
        except ValueError:
            pass

    return values_return
