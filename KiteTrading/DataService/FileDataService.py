import pickle
import Property

TRADE_SYS_FILEPATH = Property.trade_filepath


def get_trades(filepath):
    trades = []
    try:
        with open(filepath, "rb+") as file:
            trades = pickle.load(file)
    except EOFError:
        pass
    except:
        return []
    return trades


def save_trades(trades, filepath):
    with open(filepath, 'wb') as file:
        pickle.dump(trades, file)


def get_processing_trades():
    return get_trades('processing.dat')


def get_to_process_trades():
    return get_trades('to_process.dat')


def save_trade(trade):
    if trade.status == 0:
        trades = get_to_process_trades()
        if trade.trade_id not in [i.trade_id for i in trades]:
            trades.append(trade)
            save_trades(trades, 'to_process.py')
        else:
            diff = get_diff(trade, get_trade_from_trade_id(trade.trade_id))
    elif trade.status == 1:
        trades = get_processing_trades()
        if trade.trade_id not in [i.trade_id for i in trades]:
            trades.append(trade)
            save_trades(trades, 'processing.py')
        else:
            diff = get_diff(trade, get_trade_from_trade_id(trade.trade_id))

    trades = get_trades()
    if trade not in trades:
        trades.append(trade)
        save_trades(trades)


def get_trade_from_trade_id(trade_id):
    trades = get_trades()
    for trade in trades:
        if trade.trade_id == trade_id:
            return trade


def update_trade(updated_trade):
    trades = get_trades()
    for trade in trades:
        if trade.trade_id == updated_trade.trade_id:
            trade_index = trades.index(trade)
            trades[trade_index] = updated_trade
    save_trades(trades)


def get_tokens():
    tokens = []
    trades = get_trades()
    for trade in trades:
        if trade.instrument is not None:
            if trade.instrument.token is not None:
                tokens.append(trade.instrument.token)
    return tokens