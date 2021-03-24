from ..StataParser import StataCommon

from csvObject import write_csv


class RegCommon:
    def __init__(self, common_object):
        """
        Attributes found within the body of the OLS like tables

        :param common_object: An object that contains all potential output from a log file
        :type common_object: StataCommon
        """

        # Initialise the values that should be found in the table body for this table
        self.coefficients = None
        self.std_errs = None
        self.t_stats = None
        self.p_stats = None
        self.conf_95_min = None
        self.conf_95_max = None

        # Set variable names
        self.phenotype = common_object.phenotype
        self.variables = common_object.variables

    def conf_interval(self, var_key, rounding=4):
        """Set the confidence interval as a string of str((Min_CI; Max_CI)), where the CI's can be rounded"""
        return f"({round(self.conf_95_min[var_key], rounding)}; {round(self.conf_95_max[var_key], rounding)})"

    def format_for_forest(self, write_directory=None, name=None, exclusions=None, as_csv=True):
        """
        Extract information that would be used to construct a forest plot figure

        Note
        ----
        In future should have a use_blend option to just create the figure itself and cleanup all the files

        :param write_directory: Where to write the data to if writing as csv
        :type write_directory: str | Path | None

        :param name: What to call the csv file if writing as csv
        :type name: str | None

        :param exclusions: A list of names to exclude, for example _cons. Defaults to None
        :type exclusions: list[str] | None

        :param as_csv: Write the information out as a csv
        :type as_csv: bool

        :return: Rows that where to be written out or None if they where written
        :rtype: None | list[list]
        """

        # Select which variables we wish to isolate
        if exclusions is None:
            row_indexes = [i for i, _ in enumerate(self.variables)]
        else:
            row_indexes = [i for i, var in enumerate(self.variables) if var not in exclusions]

        # Isolate each rows values
        output = []
        for index, (var, coef, lb, ub) in enumerate(
                zip(self.variables, self.coefficients, self.conf_95_min, self.conf_95_max)):
            if index in row_indexes:
                output.append([var, coef, lb, ub])
        if as_csv:
            write_csv(write_directory, name, ["Phenotype", "Coefficient", "Lower Bound", "Upper Bound"], output)
        else:
            return output


class OLS(RegCommon):
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
        super().__init__(common_object)

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
        self.root_mse = self.common_obj.root_mse

        # Set the body attributes
        [setattr(self, h, [line[i] for line in self.common_obj.body]) for i, h in enumerate(self._body_headers)]

    def __repr__(self):
        """Print the regression to show what is within it"""
        return f"{self.phenotype} = {' + '.join(v for v in self.variables)}"


class HDFE(RegCommon):
    def __init__(self, common_object):
        """
        HDFE specific output

        HDFE content from reghdfe: http://scorreia.com/software/reghdfe/index.html

        Note
        ------
        When / if expanded to other log outs like R, make sure that R Common becomes an optional class that has the
        same attributes, even if forced to None.

        :param common_object: An object that contains all potential output from a log file
        :type common_object: StataCommon
        """
        super().__init__(common_object)

        # Load the common object
        self.common_obj = common_object

        # Set the attributes we want to extract for the body, HDFE has the same headers as OLS.
        self._body_headers = self.common_obj.keys.key_hdfe_headers

        # Initialise the values that should be found in the table header for this table
        self.observations = self.common_obj.observations
        self.f_stat = self.common_obj.f_stat
        self.f_prob = self.common_obj.f_prob
        self.r_sq = self.common_obj.r_sq
        self.adj_r_sqr = self.common_obj.adj_r_sqr
        self.within_r_sqr = self.common_obj.within_r_sqr
        self.root_mse = self.common_obj.root_mse
        self.adjusted_clusters = self.common_obj.adjusted_clusters

        # Set the body attributes
        [setattr(self, h, [line[i] for line in self.common_obj.body]) for i, h in enumerate(self._body_headers)]

    def __repr__(self):
        """Print the regression to show what is within it"""
        return f"{self.phenotype} = {' + '.join(v for v in self.variables)}"
