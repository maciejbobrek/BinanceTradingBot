import numpy
import pandas
from active_bots import active_bots
def algorithm(bot_id,periods=14):
    
    candles = active_bots[bot_id].candles
    close_delta = candles['close'].diff()
    close_delta = close_delta[1:]
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    

    ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()

        
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    
    if rsi[rsi.size - 1] < 30:
        return 'SELL'
    if rsi[rsi.size - 1] > 80:
        return 'BUY'
    return rsi[rsi.size - 1]
