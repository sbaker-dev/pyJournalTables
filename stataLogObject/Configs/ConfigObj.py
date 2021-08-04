from abc import ABC
from miscSupports import load_yaml
from dataclasses import dataclass, field, fields
from typing import List, Optional


LINEAR_HEADERS = ["var_name", "coefficients", "std_errs", "t_stats", "p_stats", "conf_95_min", "conf_95_max"]


@dataclass
class Header:
    extractor: str
    key_extract: int = 0
    var_type: type = float


@dataclass
class MF(ABC):
    """Model Fit base class"""
    obs: Header

    def field_names(self):
        """Returns the summary information"""
        return [f.name for f in fields(self)]


@dataclass
class LinearMF(MF):
    """Linear Regression model fit parameters"""
    f_stat: Header
    f_prob: Header
    R_sqr: Header
    r_mse: Header

    adj_r_sqr: Optional[Header] = None


# TODO
@dataclass()
class LogisticMF(MF):
    """Logistical Regression model fit parameters"""
    pass


@dataclass
class TableEntry(ABC):
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
    z_score: float


@dataclass
class PValue(TableEntry):
    p_value: float


@dataclass
class IsolateBody:
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
class Extractor:
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


@dataclass
class Table(ABC):
    mf: MF
    body_iso: IsolateBody
    table_ext: Extractor
    headers: List


@dataclass()
class TableConfigs:
    ols: Table = Table(
        LinearRHS(Header('Number of obs =', var_type=int), Header("F("), Header('Prob > F ='), Header('R-squared ='),
                  Header('Root MSE ='), Header('Adj R-squared =')),
        IsolateBody(skip_indexes=[0, 1, 2, 3, 4, 5]),
        Extractor(['Source', '|', 'SS', 'df', 'MS', 'Number', 'of', 'obs', '='], 1, [9]),
        LINEAR_HEADERS
    )

    ols_clu: Table = Table(
        LinearRHS(Header('Number of obs =', var_type=int), Header("F("), Header('Prob > F ='), Header('R-squared ='),
                  Header('Root MSE =')),
        IsolateBody(),
        Extractor(['Linear', 'regression', 'Number', 'of', 'obs', '='], 1, [6]),
        LINEAR_HEADERS
    )


class ConfigObj:
    def __init__(self, path_to_yaml):
        self._args_dict = load_yaml(path_to_yaml)

    @property
    def key_obs(self):
        """Key for extracting the number of observations"""
        return self._args_dict["Observations"]

    @property
    def key_f_stat(self):
        """Key for extracting the f stat"""
        return self._args_dict["F_Stat"]

    @property
    def key_f_prob(self):
        """Key for extracting the f probability p value"""
        return self._args_dict["F_Prob"]

    @property
    def key_r_sqr(self):
        """Key for extracting the r squared"""
        return self._args_dict["R_Sqr"]

    @property
    def key_adj_r_sqr(self):
        """Key for extracting the adjusted r squared"""
        return self._args_dict["Adj_R_Sqr"]

    @property
    def key_within_r_sqr(self):
        """Key for extracting the within r squared"""
        return self._args_dict["Within_R_Sqr"]

    @property
    def key_root_mse(self):
        """Key for extracting the root mse"""
        return self._args_dict["Root_MSE"]

    @property
    def key_adjusted_clusters(self):
        """Key for extracting the number of clusters the standard error was adjust for"""
        return self._args_dict["Adjusted_Clusters"]

    @property
    def key_ols_headers(self):
        """Headers of the table body for OLS regressions"""
        return self._args_dict["OLS_Headers"]

    @property
    def key_sum_headers(self):
        """Headers of the table body for summary stats"""
        return self._args_dict["Summary_Headers"]

    @property
    def key_tabulate_headers(self):
        """Headers to extract the tabulated body"""
        return self._args_dict["Tabulate_Headers"]

    @property
    def key_hdfe_headers(self):
        """Headers of the table body for HDFE"""
        return self._args_dict["OLS_Headers"]

    @property
    def key_fe_rsq_within(self):
        return self._args_dict["FE_Within_R_Sqr"]

    @property
    def key_fe_rsq_between(self):
        return self._args_dict["FE_Between_R_Sqr"]

    @property
    def key_fe_rsq_overall(self):
        return self._args_dict["FE_Overall_R_Sqr"]

    @property
    def key_fe_obs_per_group_min(self):
        return self._args_dict["FE_Obs_Per_Group_Min"]

    @property
    def key_fe_obs_per_group_max(self):
        return self._args_dict["FE_Obs_Per_Group_Max"]

    @property
    def key_fe_obs_per_group_avg(self):
        return self._args_dict["FE_Obs_Per_Group_Avg"]

    @property
    def key_sum_divider(self):
        """List of str required to act as the start point of a summary stat table"""
        return self._args_dict["Summary_Divider"]

    @property
    def key_ols_divider(self):
        """List of str required to act as the start point of ols output"""
        return self._args_dict["OLS_Divider"]

    @property
    def key_hdfe_divider(self):
        """List of str required to act as the start point of HDFE output"""
        return self._args_dict["HDFE_Divider"]

    @property
    def key_tab_divider(self):
        """List of str required to act as the start point of a tabulate table"""
        return self._args_dict["Tab_Divider"]

    @property
    def key_fe_within_divider(self):
        return self._args_dict["FEWithin"]
