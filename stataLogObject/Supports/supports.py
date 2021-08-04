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


def extract_values(line, skip=True):
    """Extract numerical values from a line"""

    values = [split_line.strip(ascii_letters).replace(",", "") for split_line in line.split()]

    values_return = []
    for v in values:
        try:
            values_return.append(float(v))
        except ValueError:
            if skip:
                pass
            else:
                values_return.append("MISSING")

    return values_return


def clean_value(value):
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
