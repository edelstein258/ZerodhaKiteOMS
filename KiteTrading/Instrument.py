import csv
import Property


class Instrument:

    def __init__(self, trading_symbol):
        self.trading_symbol = trading_symbol
        self.token = self.get_token(self.trading_symbol)
        self.ltp = 0

    def get_token(self, trading_symbol):
        # read from token trading_symbol map
        instrument_file_path = Property.instrument_file_path
        if instrument_file_path == '':
            print('Instrument book path Empty!!!')
            return -1

        with open(instrument_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[Property.instrument_tradingsymbol] == trading_symbol:
                    return row[Property.instrument_token]
        print('Instrument not found')
        return -1
