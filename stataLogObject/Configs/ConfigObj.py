from stataLogObject.Configs import *

from miscSupports import load_yaml
from dataclasses import dataclass
from typing import List
from abc import ABC


@dataclass
class Table(ABC):
    mf: MF
    body_iso: ExtractBody
    table_ext: ExtractTable
    headers: List


@dataclass()
class TableConfigs:
    ols: Table = Table(
        LinearMF(MFVar('Number of obs =', var_type=int), MFVar("F("), MFVar('Prob > F =', 3),
                 MFVar('R-squared =', 3), MFVar('Root MSE =', 3), MFVar('Adj R-squared =')),
        ExtractBody(skip_indexes=[0, 1, 2, 3, 4, 5]),
        ExtractTable(['Source', '|', 'SS', 'df', 'MS', 'Number', 'of', 'obs', '='], 1, [9]),
        LINEAR_HEADERS
    )

    ols_clu: Table = Table(
        LinearMF(MFVar('Number of obs =', var_type=int), MFVar("F("), MFVar('Prob > F ='),
                 MFVar('R-squared ='),
                 MFVar('Root MSE =')),
        ExtractBody(),
        ExtractTable(['Linear', 'regression', 'Number', 'of', 'obs', '='], 1, [6]),
        LINEAR_HEADERS
    )

    hdfe: Table = Table(
        LinearMF(MFVar('Number of obs =', var_type=int), MFVar("F(", 2), MFVar('Prob > F ='),
                 MFVar('R-squared ='),
                 MFVar('Root MSE ='), MFVar('Adj R-squared ='), MFVar("Within R-sq. =")),
        ExtractBody(1),
        ExtractTable(['HDFE', 'Linear', 'regression', 'Number', 'of', 'obs', '='], 1, [7]),
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
