class HeaderKeyExtractError(Exception):
    def __init__(self, index, extract_list, var_name):
        super(HeaderKeyExtractError, self).__init__(
            f"\n\tTried to extract index {index} from list {extract_list} of length {len(extract_list)} for {var_name}")


class InvalidKeyExtract(Exception):
    def __init__(self, key, var_name):
        super(InvalidKeyExtract, self).__init__(f"\n\tFailed to find {key} for {var_name}")
