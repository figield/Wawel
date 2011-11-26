
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
        self.cop = round(thermal/usage, 3)
