import json

class Variables:
    def __init__(self):
        with open('config.json') as f:
            self.var = json.load(f)

    def get(self, variable_name):
        return self.var.get(variable_name)

    def set(self, variable_name, variable_value):
        self.var[variable_name] = variable_value

    def exists(self, variable_name):
        return variable_name in self.var