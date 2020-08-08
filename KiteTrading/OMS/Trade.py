from abc import ABC,abstractmethod
from datetime import datetime

from OMS import TradeHandler, OrderHandler
from OMS.TradeType import TradeType


class Trade(ABC):
    """
    Trade parent class, different types of trade subclasses must inherit this.
    Trade subclasses are used to generalise a collective set of orders and
    positions that make up a trades management from start to finish.
    Child trade classes may be composed of positons and orders across one or
    multiple instruments and venues.
    """

    @staticmethod
    def generate_trade_id():
        return 'sys' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f')

    def __init__(self, trade_id=None, instrument=None, trade_type=None, entry_price=None, entry_trigger_price=None,
                 exit_price=None, exit_trigger_price=None, stoploss=None, trailing_stoploss=None, intraday=None,
                 quantity=None, validity=None):
        # Buy Type	Stock Name	Buy Entry	Buy Stop	Target Entry	Target Stop	Stop Loss Entry
        self.instrument = instrument
        self.trade_type = trade_type
        self.trade_size = quantity
        self.entry_price = entry_price
        self.entry_trigger_price = entry_trigger_price
        self.exit_trigger_price = exit_trigger_price
        self.exit_price = exit_price
        self.stoploss = stoploss
        self.trailing_stoploss = trailing_stoploss
        self.is_intraday = intraday
        self.entry_order_id = None
        self.exit_order_id = None
        self.entry_order_type = None
        self.entry_order_type = None
        self.entry_order_product = None
        self.status = 0                     # 0-to do    1-active     2-done      4 - rejected
        self.validity = validity
        self.trade_id = None
        if trade_id is not None:
            self.trade_id = trade_id
        else:
            self.trade_id = self.generate_trade_id()

    def enter(self, client):
        # todo add the order to Orderhandler to monitor
        if self.trade_type == TradeType.BTST:
            self.entry_order_type = client.MARKET
            # todo can NRML be used for Equity?
            self.entry_order_product = client.NRML
        elif self.trade_type == TradeType.Accumulate:
            self.entry_order_product = client.CNC
        elif self.trade_type == TradeType.Intraday:
            pass

        try:
            self.entry_order_id = client.place_order(
                variety=client.VARIETY_REGULAR,
                exchange=client.EXCHANGE_NSE,
                tradingsymbol=self.instrument.trading_symbol,
                transaction_type=client.TRANSACTION_TYPE_BUY,
                quantity=self.trade_size,
                product=client.PRODUCT_NRML,
                order_type=self.entry_order_type,
                price=self.entry_price,
                validity=self.validity
            )

            print("Entry Order placed. ID is: {}".format(self.entry_order_id))

        except Exception as e:
            print("Entry Order placement failed: {}".format(e.message))
            return -1

        self.status = 1
        OrderHandler
        return 1

    def exit(self, client):
        # todo place an exit order
        # todo add the order to Orderhandler to monitor
        try:
            self.exit_order_id = client.place_order(
                variety=client.VARIETY_REGULAR,
                exchange=client.EXCHANGE_NSE,
                tradingsymbol=self.instrument.trading_symbol,
                transaction_type=client.TRANSACTION_TYPE_SELL,
                quantity=self.trade_size,
                product=client.PRODUCT_NRML,
                order_type=client.LIMIT,
                price=self.exit_price,
                validity=self.validity
            )

            print("Exit Order placed. ID is: {}".format(self.entry_order_id))

        except Exception as e:
            print("Exit Order placement failed: {}".format(e.message))
            return -1

        self.status = 2
        return 1