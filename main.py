import tkinter as tk 
import logging
from binance_future import BinanceFuturesClient


logger = logging.getLogger()
logger.debug('This message is important only when debugging')
logger.info('This message just shows basic information')
logger.warning('Pay attention to..')
logger.error('This message helps to debug the error occurred')

logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
#file_handler.setFormatter(formater)
file_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()

if __name__ == '__main__':

    binance = BinanceFuturesClient(True)

    print(binance.get_historical_candles('BTCUSDT', '1h'))

    root = tk.Tk()

    root.mainloop()