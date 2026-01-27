class History:
    def __init__(self):
        self.history = []
    
    def add(self, command):
        self.history.append(command)
    
    def get(self):
        return self.history