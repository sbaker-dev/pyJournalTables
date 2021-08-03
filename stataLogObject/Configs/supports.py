import re


def clean_line(line):
    """
    Strip line of new line element then return, replacing negative floats without a 0, -.{value} with -0.{value}

    :param line: Line in the log file
    :type line: str
    """
    subbed = "".join([re.sub("\n", "", value) for value in line])
    return [f"-0.{v[2:]}" if v[0:2] == "-." else v for v in subbed.split(" ") if len(v) > 0]
