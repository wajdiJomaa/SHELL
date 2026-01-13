class Token:
    def __init__(self, value, is_quoted=False):
        self.value = value
        self.is_quoted = is_quoted