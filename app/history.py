class History:
    def __init__(self):
        self.history = []
        self.append_history = []
        self.session_history = []
    def add(self, command, on_startup=False):
        self.history.append(command)
        if not on_startup:
            self.session_history.append(command)
            self.append_history.append(command)


    def clear(self):
        self.append_history.clear()
    def get(self):
        return self.history