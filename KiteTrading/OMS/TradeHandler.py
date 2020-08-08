import KiteInterface
from OMS import *
from OMS.TradeStatus import TradeStatus
import Instrument


# def is_trade_active(trade):
#     return trade.status
class TradeHandler():

    def place_order(self, trade, transaction_type):
        # todo place order with kite
        pass

    def exit_all(self, trades):
        for trade in trades:
            if trade.exit():
                print(f'Trade Exited for {trade.trade_id}')

    def check_for_entry(self, trade):
        if trade.entry <= trade.instrument.ltp:
            return True
        else:
            return False

    def check_for_exit(self, trade):
        # if trade.type ==
        #     if trade.entry <= trade.instrument.ltp:
        #         return True
        #     else:
        #         return False
        ltp = trade.instrument.ltp
        if trade.status != TradeStatus.ACTIVE:
            if trade.intraday:
                if trade.trade_type == 'BUY':
                    if ltp >= trade.exit_trigger_price:
                        pass
                    elif ltp <= trade.stoploss:
                        pass
                else:
                    pass

    def run(self, trades):
        KiteInterface.login()
        while True:
            for trade in trades:
                if trade.status == 0:
                    if self.check_for_entry(trade):
                        trade.enter(KiteInterface.get_kite_client())
                elif trade.status == 1:
                    if self.check_for_exit(trade):
                        trade.exit(KiteInterface.get_kite_client())
                elif trade.status == 2:
                    print(f'trade {trade.trade_id} is processed and exited at {trade.exit_price}')
                    trades.remove(trade)

