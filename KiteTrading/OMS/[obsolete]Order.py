import datetime
from OMS import OrderStatus

ORDER_STATUS = OrderStatus()


class Order(object):

    @classmethod
    def generate_id(cls):
        return "sys" + datetime.datetime.now()

    def __init__(self,
                 exchange, trading_symbol,
                 quantity, transaction_type, order_type,
                 product, broker_id="", price=0,
                 validity=0, disclosed_quantity=0,
                 parent_order_id="", tag="", status=ORDER_STATUS.OPEN):
        self.sys_id = Order.generate_id()
        self.order_id = ""
        self.access_token = ""
        self.exchange = exchange
        self.trading_symbol = trading_symbol
        self.quantity = quantity
        self.variety = ""
        self.transaction_type = transaction_type
        self.product = product
        self.order_type = order_type
        self.broker_id = broker_id
        self.price = price
        self.validity = validity
        self.disclosed_quantity = disclosed_quantity
        self.parentOrderId = parent_order_id
        self.tag = tag
        self.status = status

    '''# Setters

    def set_sys_id(self, sys_id):
        self.sys_id = sys_id

    def set_broker_id(self, broker_id):
        self.broker_id = broker_id

    def set_exchange(self, exchange):
        self.exchange = exchange

    def set_trading_symbol(self, trading_symbol):
        self.trading_symbol = trading_symbol

    def set_variety(self, variety):
        self.variety = variety

    def set_quantity(self, quantity):
        self.quantity = quantity

    def set_transaction_type(self, transaction_type):
        self.transaction_type = transaction_type

    def set_order_type(self, order_type):
        self.order_type = order_type

    def set_price(self, price):
        self.price = price

    def set_disclosed_quantity(self, disclosed_quantity):
        self.disclosed_quantity = disclosed_quantity

    def set_parent_order_id(self, parent_order_id):
        self.parent_order_id = parent_order_id

    def set_tag(self, tag):
        self.tag = tag

    def set_status(self, status):
        self.status = status

    # Getters

    def get_sys_id(self):
        return self.sys_id

    def get_order_id(self):
        return self.order_id

    def get_exchange(self):
        return self.exchange

    def get_trading_symbol(self):
        return self.trading_symbol

    def get_variety(self):
        return self.variety

    def get_quantity(self):
        return self.quantity

    def get_transaction_type(self):
        return self.transaction_type

    def get_order_type(self):
        return self.order_type

    def get_price(self):
        return self.price

    def get_disclosed_quantity(self):
        return self.disclosed_quantity

    def get_parent_order_id(self):
        return self.parent_order_id

    def get_tag(self):
        return self.tag

    def get_status(self):
        return  self.status'''