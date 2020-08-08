import enum


class OrderStatus(enum.Enum):

    def __init__(self):
        self.OPEN = 1
        self.FILLED = 2
        self.CANCELLED = 3
        self.REJECTED = 4
        self.HELD = 5