from miscSupports import load_yaml


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
        """Headers to extract the summary body"""
        return self._args_dict["Summary_Headers"]

    @property
    def key_tabulate_headers(self):
        """Headers to extract the tabulated body"""
        return self._args_dict["Tabulate_Headers"]

    @property
    def key_sum_divider(self):
        """List of str required to act as the start point of a summary stat table"""
        return self._args_dict["Summary_Divider"]

    @property
    def key_ols_divider(self):
        """List of str required to act as the start point of ols output"""
        return self._args_dict["OLS_Divider"]

    @property
    def key_tab_divider(self):
        """List of str required to act as the start point of a tabulate table"""
        return self._args_dict["Tab_Divider"]