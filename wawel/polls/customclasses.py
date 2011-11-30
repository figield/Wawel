
class Cost:
    def __init__(self, period, usage, cost):
        self.period = period
        self.usage = usage
        self.cost = cost

class Usage:
    def __init__(self, period, usage, cost, thermal):
        self.period = period
        self.usage = usage
        self.cost = cost
        self.thermal = thermal
        if usage == 0:
            self.cop = 0
        else:
            self.cop = round(thermal/usage, 3)
