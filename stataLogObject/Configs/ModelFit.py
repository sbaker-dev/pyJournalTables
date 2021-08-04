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

    def field_names(self):
        """Returns the summary information"""
        return [f.name for f in fields(self)]


@dataclass
class LinearMF(MF):
    """Linear Regression model fit parameters"""
    obs: MFVar
    f_stat: MFVar
    f_prob: MFVar
    r_sqr: MFVar
    r_mse: MFVar

    adj_r_sqr: Optional[MFVar] = None
    within_r_sqr: Optional[MFVar] = None


@dataclass
class TabMF(MF):
    total: MFVar


@dataclass
class PanelMF(MF):
    obs: MFVar
    groups: MFVar
    obs_group_min: MFVar
    obs_group_avg: MFVar
    obs_group_max: MFVar
    f_stat: MFVar
    f_prob: MFVar
    r_sqr_within: MFVar
    r_sqr_between: MFVar
    r_sqr_overall: MFVar
    sigma_u: MFVar
    sigma_e: MFVar
    rho: MFVar


# TODO
@dataclass
class LogisticMF(MF):
    """Logistical Regression model fit parameters"""
    pass
