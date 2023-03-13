from binance.client import Client
from binance import exceptions as binance_excp
from flask_login import current_user
import dummy_config
class Client_Wrapper():
    def __init__(self,public=dummy_config.API_PUBLIC,secret=dummy_config.API_SECRET,tld='com'):
            try:
                self.Client = Client(public, secret, tld=tld)
                if public != dummy_config.API_PUBLIC and secret != dummy_config.API_SECRET:
                    self.Client.create_test_order(symbol='ETHUSDT',side='BUY',type='MARKET',quantity=10)
                
                print("Client_Wrapper object: ", self)
            except Exception as e:
                print("Client init error: ", e)
    
    def set_dummy(self):
        self.Client = Client(dummy_config.API_PUBLIC, dummy_config.API_SECRET, tld='com')
        print( "set_dummy: ", self)

    def set_Client(self):
        try:
            for bot in current_user.bots:
                    self.Client = Client(bot.public,bot.secret, tld='com')
                    self.Client.create_test_order(symbol='ETHUSDT',side='BUY',type='MARKET',quantity=10)
                    print("set_Client: ", self)
                    break
            return True
        except Exception as e:
            if e == binance_excp:
                if e.code == -2015:
                    print("set_Client error: ",e)
            print("set_Client error: ", e)
            return False
    
    def get_balances(self):
        balances = []
        try:
            account = self.Client.get_account()
            for balance in account['balances']:
                if float(list(balance.values())[1]) != 0.0 or float(list(balance.values())[2]) != 0.0:
                    balances.append(balance)
            return balances
        except Exception as e:
             print("Account check failed: ",e)
                      
    def __str__(self):
        return f'Binance Client \n Public: {self.Client.API_KEY} \n Secret: {self.Client.API_SECRET}'
                
client = Client_Wrapper(dummy_config.API_PUBLIC, dummy_config.API_SECRET, tld='com')
