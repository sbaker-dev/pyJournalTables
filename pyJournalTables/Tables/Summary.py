from ..StataParser import StataCommon

from csvObject import write_csv


class SummaryStats:
    def __init__(self, common_object):
        """
        Summary Stats akin to stata 'sum' specific output

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
        self._body_headers = self.common_obj.keys.key_sum_headers

        # Initialise the values that should be found in the table body for this table
        self.obs = None
        self.mean = None
        self.std_dev = None
        self.min = None
        self.max = None

        # Set the body attributes
        [setattr(self, h, [line[i] for line in self.common_obj.body]) for i, h in enumerate(self._body_headers)]

        # Set variable names
        self.variables = self.common_obj.variables

    def __repr__(self):
        """Print how many outcomes we have summary data for"""
        return f"Summary Stats of {len(self.variables)} variables"

    def write_csv(self, output_directory, file_name, alt_variable_names=None):
        """Construct the summary information into a csv file"""

        # If alternative names are provided use those instead
        if alt_variable_names:
            assert len(alt_variable_names) == self.variables
            variables = alt_variable_names
        else:
            variables = self.variables

        row_content = [[var, int(obs), mean, std_dev, mi, ma] for var, obs, mean, std_dev, mi, ma in zip(
            variables, self.obs, self.mean, self.std_dev, self.min, self.max)]
        write_csv(output_directory, file_name, ["Variable", "Observations", "Mean", "Standard Deviation", "Min", "Max"],
                  row_content)
