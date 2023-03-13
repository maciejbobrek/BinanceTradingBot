from flask import Blueprint,render_template,redirect,url_for,request,flash,jsonify
from binance.client import Client
from binance import exceptions
import threading,time,pandas
from importlib import import_module
from db_Models import *
from websocket_manager import Binance_WS
from active_bots import active_bots
from flask import Request
class Bot_Daemon():
    def __init__(self,client,bot_id,symbol,quantity,period,algorithm) -> None:
        self.client = client
        self.bot_id = bot_id
        self.algorithm = algorithm
        self.symbol = symbol
        self.quantity = quantity
        self.period = period
        self.candles = pandas.DataFrame()
        self.set_candles()

    def __del__(self):
        print("Bot " + self.bot_id + " shut down")
        
    def run_task(self):
        ws_thread = threading.Thread(target=self.run_websocket)
        ws_thread.daemon = True
        ws_thread.start()
        active_bots[self.bot_id] = self

    def run_websocket(self): 
        url = 'wss://stream.binance.com:9443/ws/'+ self.symbol.lower() + '@kline_' + self.period
        Binance_WS(stream_url = url,bot_id = self.bot_id)
        if active_bots.get(self.bot_id) != None:
            self.run_websocket()

    def set_candles(self):
        try:
            if self.candles.empty:
                candlesticks = self.client.get_historical_klines(self.symbol,self.period, str(int(time.time())-60*60*24),str(int(time.time())))
                
                processed_candlesticks = []
                for candle_data in candlesticks:
                    candlestick = { 
                        "time": float(candle_data[0]) / 1000.0, 
                        "open": float(candle_data[1]),
                        "high": float(candle_data[2]), 
                        "low": float(candle_data[3]), 
                        "close": float(candle_data[4]),
                    }
                    processed_candlesticks.append(candlestick)
                self.candles = pandas.DataFrame(processed_candlesticks)
        except Exception as e:
            print("Error: " + str(e))

    def execute_order(self,side,order_type='MARKET'):
        try:
            print("sending order")
            order = self.client.create_order(symbol=self.symbol, quantity=self.quantity, side=side,type=order_type)
            print(order)
        except Exception as e:
            print("an exception occured - {}".format(e))
            return False

        return True  
   
    
def load_algo(bot_id):
    algo = getattr(import_module("algorithm.algorithm_"+ bot_id), 'algorithm')
    return algo


def load_default_algo():
    algo = getattr(import_module("algorithms.default_algorithm"),'algorithm')
    return algo



def activate_bot(bot_id, symbol,quantity,period):
        if bot_id in active_bots.keys():
            return False
        try:
            client = Client(Bot.query.filter_by(id=bot_id).first().public,Bot.query.filter_by(id=bot_id).first().secret, tld='com')
            client.create_test_order(symbol='ETHUSDT', side='BUY', type='MARKET', quantity=100)
            algo = load_default_algo()
            bot_daemon = Bot_Daemon(client,bot_id, symbol,quantity,period,algo)
            bot_daemon.run_task()
            bot = Bot.query.get(bot_id)
            bot.uptime = time.time()
            db.session.commit()
        except Exception as err:
            flash("Failed to activate bot: " + Bot.query.filter_by(id=bot_id).first().keylabel + '\n' + str(err), category='error')

def shutdown_bot(bot_id):
    print(active_bots)
    active_bots.pop(bot_id)
    print(active_bots)
    bot = Bot.query.get(bot_id)
    bot.uptime = 0.0
    db.session.commit()
 
def reset_uptime():
    """
        In case of a unexpected closing of the app reset the bots uptime
    
    """
    for bot in db.session.query(Bot).all():    
        if bot.uptime > 0.0 and active_bots.get(bot.id) == None:
                bot.uptime = 0.0
                db.session.commit()