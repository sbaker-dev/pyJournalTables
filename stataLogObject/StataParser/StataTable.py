from stataLogObject.StataParser import StataRaw
from stataLogObject.Configs.ConfigObj import TableExtractions, RHSHeaders, RHS, Header
from stataLogObject.Configs.supports import extract_values
from stataLogObject.Configs.Errors import HeaderKeyExtractError, InvalidKeyExtract

from pathlib import Path


class StataTable:
    def __init__(self, raw_table, supporting):
        """

        :param raw_table: The raw table from StataRaw object
        :type raw_table: list[list]

        :param supporting: The supporting information above the table body containing Header class attributes
        :type supporting: RHS
        """

        # Raw table reference
        self._raw = raw_table

        # Set the supporting table header values
        [setattr(self, s, self.set_header_value(getattr(supporting, s), s)) for s in supporting.supporting_fields()]

    def set_header_value(self, header, var_name):
        """

        :param header:
        :type header: Header

        :param var_name: The name of this header for Error Handling
        :type var_name: str

        :return: The numeric values of the header supporting values
        :rtype: float | int

        :raises HeaderKeyExtractError InvalidKeyExtract: If the header.key_extract leads to a KeyError and No line found
            for header.extractor respectively
        """
        for line in self._raw:

            line_str = " ".join(line)
            if header.extractor in line_str:
                values = extract_values(line_str)
                try:
                    return header.var_type(values[header.key_extract])
                except KeyError:
                    raise HeaderKeyExtractError(header.key_extract, values)

        raise InvalidKeyExtract(header.extractor, var_name)


c = StataRaw(Path(r"C:\Users\Samuel\PycharmProjects\stataLogObject\DoLogs\MultiTableLog.log"),
             TableExtractions().ols)

#
for t in c.raw_tables:
    StataTable(t, RHSHeaders().ols)
    break







# [StataTable(t, RHSHeaders().ols) for t in c.raw_tables]