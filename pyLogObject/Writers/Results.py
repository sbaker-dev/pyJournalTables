from csvObject import CsvObject
from pathlib import Path


def write_forest_methods(forest_csv, out_dir, out_name):
    """
    Write out a results section of risk differences from a forest csv

    :param forest_csv: Path to a csv with variable name, coefficent, CI min, CI Max
    :type forest_csv: Path | str

    :param out_dir: Out directory
    :type out_name: Path | str

    :param out_name: Name of the out file
    :type out_name: str

    :return: Nothing
    :rtype: None
    """

    # Load the forest data
    csv_obj = CsvObject(forest_csv)

    # Create the lines
    lines_list = []
    for name, coefficient, bound_min, bound_max in csv_obj.row_data:
        rd = f"(RD={round(float(coefficient), 2)}, 95%CI: {round(float(bound_min), 2)}; {round(float(bound_max), 2)})"
        lines_list.append(f"{name} {rd}\n")

    # Write the line data
    with open(Path(out_dir, f"{out_name}.md"), "w") as f:
        for line in lines_list:
            f.write(line)
