import enum


class TradeStatus(enum.Enum):

    def __init__(self):
        self.TODO = 1
        self.ACTIVE = 2
        self.DONE = 3
        self.REJECTED = 4
