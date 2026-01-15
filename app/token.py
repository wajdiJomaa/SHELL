class Token:
    def __init__(self, value, is_quoted=False, is_double_quote=False):
        self.value = value
        self.is_quoted = is_quoted
        self.is_double_quote = is_double_quote
