from OMS import Order
from OMS import OrderStatus

ORDER_STATUS = OrderStatus()


class BracketOrder(Order):

    def __init__(
            self, exchange, trading_symbol,
            quantity, transaction_type, order_type,
            product, stoploss, squareoff, trailing_stoploss=0,
            broker_id="", price=0,
            validity=0, disclosed_quantity=0,
            parent_order_id="", tag="", status=ORDER_STATUS.OPEN):
        super().__init__(
            exchange, trading_symbol,
            quantity, transaction_type, order_type,
            product, broker_id, price,
            validity, disclosed_quantity,
            parent_order_id, tag, status)
        self.stoploss = stoploss
        self.square_off = squareoff
        self.trailing_stoploss = trailing_stoploss
