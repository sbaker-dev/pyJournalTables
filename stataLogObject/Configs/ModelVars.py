from stataLogObject.Supports import HeaderKeyExtractError, InvalidKeyExtract, extract_values

from dataclasses import dataclass, field
from typing import List
from abc import abstractmethod


@dataclass
class VarField:
    extractor: str
    var_type: type = float

    def find_mf(self, lines_list, var_name):
        """Find the model fit parameter in the lines list"""
        for i, line in enumerate(lines_list):
            if self.extractor in " ".join(line):
                return self._extract_mf(i, lines_list, var_name)

        raise InvalidKeyExtract(self.extractor, var_name)

    @abstractmethod
    def _extract_mf(self, index, lines_list, var_name):
        """Extract the model fit parameter(s) from the raw table"""

    @abstractmethod
    def _extract_var(self, values_list, var_name):
        """Extract the variable(s) from the list of values for a given variable"""


@dataclass
class MFVar(VarField):
    """Extracting information for a given model fit variable"""
    key_extract: int = 0

    def _extract_mf(self, index, lines_list, var_name):
        values = extract_values(" ".join(lines_list[index]))

        if len(values) == 0:
            print(f"Warning: {var_name} not set yet requested")
            return "N/A"
        else:
            return self._extract_var(values, var_name)

    def _extract_var(self, values_list, var_name):
        try:
            return self.var_type(values_list[self.key_extract])
        except (KeyError, IndexError):
            raise HeaderKeyExtractError(self.key_extract, values_list, var_name)


@dataclass
class REVar(VarField):
    """Random effects parameters"""
    key_extract: List = field(default_factory=lambda: [0, 1, 2, 3])
    re_headers: List = field(default_factory=lambda: ["Est", "Std Err", "LB_95", "UB_95"])

    def _extract_mf(self, index, lines_list, var_name):
        # Extract each random parameter as a dict
        random_params = [self._extract_var(line, var_name) for i, line in enumerate(lines_list)
                         if i > index and ("|" in line) and (":" not in " ".join(line))]

        # Merge the dicts into a master dict to return
        return {f"{list(rp.keys())[0]}_{i}": list(rp.values())[0] for i, rp in enumerate(random_params)}

    def _extract_var(self, values_list, var_name):

        # Set this variable name from the elements that are not the last 4
        var_name = " ".join(values_list[:-4]).strip("|").strip(" ")

        # Extract the values that are the last 4, SE calculation can fail so allow for missing
        values = extract_values(" ".join(values_list[-4:]), False)
        if len(values) == 0:
            print(f"Warning: {var_name} not set yet requested")
            return "N/A"

        # For each key in RE return the header-value of the random effects parameters
        try:
            return {var_name: {h: values[i] if values[i] == "MISSING" else self.var_type(values[i])
                               for h, i in zip(self.re_headers, self.key_extract)}}
        except (KeyError, IndexError):
            raise HeaderKeyExtractError(self.key_extract, values, var_name)

