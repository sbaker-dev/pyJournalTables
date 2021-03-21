class TableObj:
    def __init__(self, raw_table):
        self.raw_table = raw_table

        # Supporting statistics (individual ints/floats)
        self.observations = None
        self.f_stat = None
        self.f_prob = None
        self.r_sqr = None
        self.adj_r_sqr = None
        self.within_r_sqr = None
        self.root_mse = None
        self.adjusted_clusters = None

        # Outcome variables (string and list of strings)
        self.phenotype = None
        self.variables = None

        # Outcome Statistics (floats in rows, where each row represents a coefficient)
        self.coefficients = None
        self.std_errs = None
        self.t_stats = None
        self.p_stats = None
        self.conf_95_min = None
        self.conf_95_max = None

        pass

    def conf_interval(self, var_key, rounding=4):
        return f"({round(self.conf_95_min[var_key], rounding)} to {round(self.conf_95_max[var_key], rounding)})"
