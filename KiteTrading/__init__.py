import StreamLiveData
# from OMS.TradeHandler import TradeHandler
import ReadOrders
import threading
# from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

trades = []

# todo read start ReadOrder
# read_order = threading.Thread(target=ReadOrders.run, name='ReadOrders')
# read_order = Process(target=ReadOrders.run, name='ReadOrders')


# Start streaming of Data
# Streaming of tick data
# stream_live_data = threading.Thread(target=StreamLiveData.run, name='StreamLiveData')
# stream_live_data = Process(target=StreamLiveData.run, name='StreamLiveData')

# read_order.start()
# stream_live_data.start()

#
# # todo read start TradeHandler
# trade_handler = TradeHandler()
# trade_handler.run(trades)

# read_order.join()
# stream_live_data.join()
def main():
    # todo assign names to thread pool
    with ThreadPoolExecutor() as executor:
        read_order = executor.submit(ReadOrders.run)
        stream_live_data = executor.submit(StreamLiveData.run)


if __name__ == '__main__':
    main()
    # with ProcessPoolExecutor() as executor:
    #     read_order = executor.submit(ReadOrders.run)
    #     stream_live_data = executor.submit(StreamLiveData.run)
        # read_order.result()
        # stream_live_data.result()
