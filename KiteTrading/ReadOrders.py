import csv
import logging
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import DataService.FileDataService as DataService
from OMS.Trade import Trade
from Instrument import Instrument
import Property
from OMS.TradeType import TradeType

TRADE_FILEPATH = Property.csv_trade_filepath


def read_trade_csv():
    trade_csv_list = []
    if TRADE_FILEPATH == '':
        print('Trade book path Empty!!!')
        return -1
    with open(TRADE_FILEPATH, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            trade_csv_list.append(row)
    if len(trade_csv_list) == 0:
        return -1
    return trade_csv_list


def get_instrument(instrument_name):
    ins = Instrument(instrument_name.replace(" ", ""))
    if ins is None:
        print(f'Error while fetching instrument {instrument_name}')
        return -1
    if ins.token == -1:
        return -1
    return ins


# def get_tokens(insturments):
#     tokens = []
#     for ins in insturments:
#         tokens.append(ins.token)
#     return tokens


def create_trade(trade_csv):
    if trade_csv[Property.csv_trade_id] != '':
        trade = Trade()
    else:
        trade = Trade(trade_id=trade_csv[Property.csv_trade_id])

    trade.trade_size = trade_csv[Property.csv_trade_size]
    trade.stoploss = trade_csv[Property.csv_stoploss]

    ins = get_instrument(trade_csv[Property.csv_instrument_name])
    if ins == -1:
        logging.error(f'Could not fetch {trade_csv[Property.csv_instrument_name]} for trade {trade_csv}')
        return None
    if trade_csv[Property.csv_trade_type].replace(" ", "") == TradeType.IntraDay.value:
        trade = Trade(
            instrument=ins,
            trade_type=TradeType.IntraDay,
            entry_price=trade_csv[Property.csv_entry],
            entry_trigger_price=trade_csv[Property.csv_entry_trigger],
            exit_price=trade_csv[Property.csv_traget],
            exit_trigger_price=trade_csv[Property.csv_target_trigger],
            stoploss=trade_csv[Property.csv_stoploss],
            # trailing_stoploss=trade_csv[Property.csv_trailing_stoploss],
            intraday=True,
            quantity=trade_csv[Property.csv_trade_size],
            # validity=trade_csv[Property.csv_trade_validity]
        )
    return trade


# def update_trades(trade_csv_list):
#     for row in trade_csv_list:
#         if row[Property.csv_status] != '2':
#             trade = create_trade(row)
#             if trade is not None:
#                 update_csv(row, 0)


def update_csv(updated_row, status, trade_id=None):
    old_file = []
    with open(TRADE_FILEPATH, 'r+') as file:
        reader = csv.DictReader(file)
        for row in reader:
            old_file.append(row)

    with open(TRADE_FILEPATH, 'w+', newline='\n') as file:
        writer = csv.DictWriter(file, fieldnames=updated_row.keys())
        writer.writeheader()
        for row in old_file:
            if row == updated_row:
                updated_row[Property.csv_status] = status
                if trade_id is not None:
                    updated_row[Property.csv_trade_id] = trade_id
                writer.writerow(updated_row)
            else:
                writer.writerow(row)

    return


# ================================================ Script Begins Here ============================================== #

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        trades_csv = read_trade_csv()
        process_trades(trades_csv)


def get_trades_to_process(trades_csv):
    trades_to_process = []
    for row in trades_csv:
        if row[Property.csv_status] == '':
            trade = create_trade(row)
            trades_to_process.append(trade)
            update_csv(row, '0', trade.trade_id)
        if row[Property.csv_status] == '0':
            trade = create_trade(row)
            if row[Property.csv_trade_id] == '':
                update_csv(row, '0', trade.trade_id)
            trades_to_process.append(trade)
    return trades_to_process


def get_trades_processing(trades_csv):
    trades_processed = []
    for row in trades_csv:
        if row[Property.csv_status] == '1':
            trades_processed.append(create_trade(row))
    return trades_processed


def process_trades(trades_csv):
    trades_to_process = get_trades_to_process(trades_csv)
    trades_processing = get_trades_processing(trades_csv)
    DataService.get_to_process_trades()
    DataService.save_trades(trades_to_process)


def run():
    trades_csv = read_trade_csv()
    process_trades(trades_csv)
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=TRADE_FILEPATH, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
