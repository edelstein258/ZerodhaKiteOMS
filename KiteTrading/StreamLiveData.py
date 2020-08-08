import logging
import time

from KiteInterface import get_ticker
from DataService.FileDataService import *


logging.basicConfig(level=logging.DEBUG)

# Callback for tick reception.
def update_ltp():
    pass


def on_ticks(ws, ticks):
    if len(ticks) > 0:
        for tick in ticks:
            # todo get ltp for tokens and update ltp for each instrument
            pass
        update_ltp()


# Callback for successful connection.
def on_connect(ws, response):
    tokens = []
    logging.info("Successfully connected. Response: {}".format(response))
    while len(tokens) == 0:
        print("Tokens empty - Fetching tokens")
        tokens = get_tokens()
        time.sleep(10)
    try:
        ws.subscribe(tokens)

        ws.set_mode(ws.MODE_FULL, tokens)
    except:
        logging.error("Could not subscribe the tokens")
    logging.info("Subscribe to tokens in Full mode: {}".format(tokens))


# Callback when current connection is closed.
def on_close(ws, code, reason):
    logging.info("Connection closed: {code} - {reason}".format(code=code, reason=reason))


# Callback when connection closed with error.
def on_error(ws, code, reason):
    logging.info("Connection error: {code} - {reason}".format(code=code, reason=reason))


# Callback when reconnect is on progress
def on_reconnect(ws, attempts_count):
    logging.info("Reconnecting: {}".format(attempts_count))


# Callback when all reconnect failed (exhausted max retries)
def on_noreconnect(ws):
    logging.info("Reconnect failed.")


def run():
    # Initialise

    kws = get_ticker()
    # Assign the callbacks.
    kws.on_ticks = on_ticks
    kws.on_close = on_close
    kws.on_error = on_error
    kws.on_connect = on_connect
    kws.on_reconnect = on_reconnect
    kws.on_noreconnect = on_noreconnect

    # Infinite loop on the main thread. Nothing after this will run.
    # You have to use the pre-defined callbacks to manage subscriptions.
    kws.connect(threaded=True)