from ..StataParser import StataCommon


class HDFE:
    def __init__(self, common_object):
        """
        OLS specific output

        Note
        ------
        When / if expanded to other log outs like R, make sure that R Common becomes an optional class that has the
        same attributes, even if forced to None.

        :param common_object: An object that contains all potential output from a log file
        :type common_object: StataCommon
        """

        # Load the common object
        self.common_obj = common_object

        # Set the attributes we want to extract for the body
        self._body_headers = self.common_obj.keys.key_ols_headers

        # Initialise the values that should be found in the table header for this table
        self.observations = self.common_obj.observations
        self.f_stat = self.common_obj.f_stat
        self.f_prob = self.common_obj.f_prob
        self.r_sq = self.common_obj.r_sq
        self.adj_r_sqr = self.common_obj.adj_r_sqr
        self.within_r_sqr = self.common_obj.within_r_sqr
        self.root_mse = self.common_obj.root_mse
        self.adjusted_clusters = self.common_obj.adjusted_clusters

        # Initialise the values that should be found in the table body for this table
        self.coefficients = None
        self.std_errs = None
        self.t_stats = None
        self.p_stats = None
        self.conf_95_min = None
        self.conf_95_max = None

        # Set the body attributes
        [setattr(self, h, [line[i] for line in self.common_obj.body]) for i, h in enumerate(self._body_headers)]

        # Set variable names
        self.phenotype = self.common_obj.phenotype
        self.variables = self.common_obj.variables

    def __repr__(self):
        """Print the regression to show what is within it"""
        return f"{self.phenotype} = {' + '.join(v for v in self.variables)}"

    def conf_interval(self, var_key, rounding=4):
        """Set the confidence interval as a string of str((Min_CI; Max_CI)), where the CI's can be rounded"""
        return f"({round(self.conf_95_min[var_key], rounding)}; {round(self.conf_95_max[var_key], rounding)})"
