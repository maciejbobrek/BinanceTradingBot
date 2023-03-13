import websocket, json,logging
from pandas import DataFrame
from active_bots import active_bots
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
class Binance_WS():
    def __init__(self,stream_url,bot_id):
        websocket.enableTrace(False)
        self.bot_id = bot_id
        self.stream_url = stream_url
        self.ws = websocket.WebSocketApp(url=stream_url,
                                         on_message= self.listener, 
                                         on_error= self.on_error, 
                                         on_close= self.on_close,
                                         on_open = self.on_open)
        self.ws.run_forever()
    def on_open(self,ws):
        logging.info('Bot ' + str(self.bot_id) + " started listening to: " + str(self.stream_url))
        
    def on_close(self,ws):
        logging.info('Bot ' + str(self.bot_id) + " closed connection: " + str(self.stream_url))
        
    def on_error(self,ws,error):
        logging.info('Bot ' + str(self.bot_id) + " connection error: " + str(self.stream_url))
        logging.info(str(error))
        
    def listener(self,ws,msg):
        """
            Bot listening to a given exchange rate and acting upon a given algorithm
        Args:
            BinanceWS (WebSocket): websocket listening to the exchange rate of the open position
            message (JSON): the latest candlestick received from the exchange
        """
        if active_bots.get(self.bot_id) == None:
            logging.info("closing")
            ws.close()
            
        json_message = json.loads(msg)
        candle = DataFrame([self.process_candle(json_message)])
        log_msg = 'Timestamp: ' + str(json_message['E']) +' | Bot ' + str(self.bot_id) + " received message from: " + str(self.stream_url)
        logging.info(log_msg)
        signal = None
        try:
            logging.info("Bot " + str(self.bot_id) + " RSI:" + str(active_bots[self.bot_id].algorithm(self.bot_id)))
            # active_bots[self.bot_id].candles = active_bots[self.bot_id].candles.join(candle)
            signal = active_bots[self.bot_id].algorithm(self.bot_id) 
        except Exception as e:
            logging.info(str(e))
            
        if signal == 'BUY' or signal == 'SELL':
            self.request_order(signal)
        
        
    def process_candle(self,candle_data):

        candlestick = { 
                        "time": float(candle_data['E']) / 1000.0, 
                        "open": float(candle_data['k']['t']),
                        "high": float(candle_data['k']['T']), 
                        "low": float(candle_data['k']['l']), 
                        "close": float(candle_data['k']['h'])
        }
        return candlestick
    
    def request_order(self,signal):
        try:
            if signal == 'BUY':
                self.order('BUY')
            elif signal == 'SELL':
                self.order('SELL')
        except Exception as e:
            logging.info("{}".format(e))        
    
    
        

