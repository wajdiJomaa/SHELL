class History:
    def __init__(self):
        self.history = []
        self.append_history = []
    def add(self, command):
        self.history.append(command)
        self.append_history.append(command)

    def clear(self):
        self.append_history.clear()
    def get(self):
        return self.history