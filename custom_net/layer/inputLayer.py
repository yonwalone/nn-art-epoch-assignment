class InputLayer:

    def __init__(self, inputs, bias) -> None:
        self.values = inputs
        self.values.append(bias)
        pass

    def act(self):
        return self.values