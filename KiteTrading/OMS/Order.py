from abc import ABC
from OMS.OrderStatus import OrderStatus


class Order(ABC):
    """
    Trade parent class, different types of trade subclasses must inherit this.
    Trade subclasses are used to generalise a collective set of orders and
    positions that make up a trades management from start to finish.
    Child trade classes may be composed of positons and orders across one or
    multiple instruments and venues.
    """
    def __init__(self, order_id):
        self.order_id = order_id
        self.status = OrderStatus.OPEN

    def execute(self):
        pass

    def get_status(self):
        pass