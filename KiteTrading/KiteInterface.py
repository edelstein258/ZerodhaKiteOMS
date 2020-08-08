import pickle
from datetime import datetime, timedelta, time
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-9s) %(message)s',)

from kiteconnect import KiteConnect
from kiteconnect import KiteTicker

import Property

session = {}


def get_kite_client():
    """Returns a kite client object
    """
    kite = KiteConnect(Property.api_key)
    if "access_token" in session.keys():
        kite.set_access_token(session["access_token"])
    else:
        logging.warn("Access token not found in Session variable")
        return -1
    return kite


def get_kite_login_url():
    kite = get_kite_client()
    return kite.login_url()


def get_request_token():
    print(get_kite_login_url())
    return input('Enter the Request token, use the above url to login')


def load_session():
    global session
    logging.info("Trying to fetch session variable from system")
    try:
        with open(Property.session_filepath, 'rb+') as file:
            session = pickle.load(file)
    except:
        logging.warn('No session variable found in system')
        return -1
    logging.info("Session variable loaded successfully from system")
    return 1


def save_session():
    session['saved_time'] = datetime.now()
    with open(Property.session_filepath, 'wb+') as file:
        pickle.dump(session, file)


def login():
    logging.info('Trying to Login to Kite')
    global session
    try:
        kite = kite = KiteConnect(Property.api_key)
        request_token = get_request_token()
        session = kite.generate_session(request_token, api_secret=Property.api_secret)
        now = datetime.strptime(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        if now.time() < time(7, 30):
            session['access_token_valid_till'] = now.replace(hour=7, minute=30, second=0, microsecond=0)
        else:
            session['access_token_valid_till'] = (now + timedelta(days=1)).replace(hour=7, minute=30, second=0,microsecond=0)
        kite.set_access_token(session['access_token'])
        session['request_token'] = request_token
        save_session()
    except Exception as e:
        logging.warn('Exception occurred during login', e)
        return -1
    logging.info('Login successful')
    return 1


def access_token_valid():
    if 'access_token_valid_till' in session.keys():
        if session['access_token_valid_till'] > datetime.now():
            logging.info("current access_token is valid")
            return True
        logging.info(f"current access_token is not valid or not present in locally {session['access_token_valid_till']}")
    return False


def get_ticker():
    load_session()
    if access_token_valid():
        return KiteTicker(Property.api_key, session['access_token'])
    else:
        logging.info('No access token found!!')
        while login() == -1:
            pass
        return KiteTicker(Property.api_key, session['access_token'])
