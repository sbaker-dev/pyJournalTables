from dataclasses import dataclass, fields
from typing import Optional
from abc import ABC


@dataclass
class MFVar:
    """Extracting information for a given model fit variable"""
    extractor: str
    key_extract: int = 0
    var_type: type = float


@dataclass
class MF(ABC):
    """Model Fit base class"""
    obs: MFVar

    def field_names(self):
        """Returns the summary information"""
        return [f.name for f in fields(self)]


@dataclass
class LinearMF(MF):
    """Linear Regression model fit parameters"""
    f_stat: MFVar
    f_prob: MFVar
    R_sqr: MFVar
    r_mse: MFVar

    adj_r_sqr: Optional[MFVar] = None
    within_r_sqr: Optional[MFVar] = None


# TODO
@dataclass()
class LogisticMF(MF):
    """Logistical Regression model fit parameters"""
    pass
