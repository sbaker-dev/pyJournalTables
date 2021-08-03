from miscSupports import load_yaml
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass()
class RightHandSupports:
    """The right hand side of the supporting information in the log at the top of each table"""
    obs: List = field(default_factory=lambda: ['Number', 'of', 'obs', '='])
    f_stat: List = field(default_factory=lambda: ["F("])
    f_prop: List = field(default_factory=lambda: ['Prob', '>', 'F', '='])
    r_sqr: List = field(default_factory=lambda: ['R-squared', '='])
    adj_r_sqr: List = field(default_factory=lambda: ['Adj', 'R-squared', '='])
    within_r_sqr: List = field(default_factory=lambda: ['Within', 'R-sq.'])
    root_mse: List = field(default_factory=lambda: ['Root', 'MSE', '='])
    adj_clusters: List = field(default_factory=lambda: ['(Std.', 'Err.', 'adjusted', 'for'])


@dataclass()
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


@dataclass()
class TableExtractions:
    ols: Extractor = Extractor(['Source', '|', 'SS', 'df', 'MS', 'Number', 'of', 'obs', '='], 1, [9])
    hdfe: Extractor = Extractor(['HDFE', 'Linear', 'regression', 'Number', 'of', 'obs', '='], 1, [7])
    summary: Extractor = Extractor(['Variable', '|', 'Obs', 'Mean', 'Std.', 'Dev.', 'Min', 'Max'], 0)
    tab: Extractor = Extractor(['|', 'Freq.', 'Percent', 'Cum.'], 0, [0])
    fe_within: Extractor = Extractor(['Fixed-effects', '(within)', 'regression', 'Number', 'of', 'obs', '='], 3, [7])


@dataclass
class TableHeaders:
    """Contains the headers of each table type"""
    reg: List = field(
        default_factory=lambda: ["coefficients", "std_errs", "t_stats", "p_stats", "conf_95_min", "conf_95_max"])
    summary: List = field(default_factory=lambda: ["obs", "mean", "std_dev", "min", "max"])
    tab: List = field(default_factory=lambda: ["frequency", "percent", "cumulative"])


@dataclass
class ConfigObj2:
    """This contains configurations for extraction for each element in a log"""

    right_supports: RightHandSupports = RightHandSupports()
    isolates: TableExtractions = TableExtractions()
    table_headers: TableHeaders = TableHeaders()


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
