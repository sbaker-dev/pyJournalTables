from dataclasses import dataclass, fields
from abc import ABC

LINEAR_HEADERS = ["var_name", "coefficients", "std_errs", "t_stats", "p_stats", "conf_95_min", "conf_95_max"]


@dataclass
class TableEntry(ABC):
    """The entries for a given table's variable"""
    var_name: str
    coefficient: float
    std_err: float
    prob: float
    lb_95: float
    ub_95: float

    def entry_values(self):
        """Get all the values associated with this entry"""
        return {f.name: getattr(self, f.name) for f in fields(self)}


@dataclass
class ZScore(TableEntry):
    """Z score variant of TableEntry"""
    z_score: float


@dataclass
class PValue(TableEntry):
    """P value variant of Table Entry"""
    p_value: float

