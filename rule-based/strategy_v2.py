import pandas as pd
from ta.trend import EMAIndicator
from scipy.signal import find_peaks
import numpy as np
from datetime import datetime
import logging

class TradingStrategy:
    def __init__(self, lot_size=10000):
        self.lot_size = lot_size

    def prepare_data(self, df):
        df["EMA50"] = EMAIndicator(df["5min_close"], window=50, fillna=False).ema_indicator()
        return df

    def calculate_trendline(self, data_5min):
        x = np.arange(len(data_5min))
        y = data_5min['low']['close'].values
        slope, intercept = np.polyfit(x, y, 1)
        return slope, intercept

    def find_entry_point(self, data_1min, trendline):
        x = np.arange(len(data_1min))
        trendline_values = trendline[0] * x + trendline[1]
        below_trendline = data_1min['close'].values <= trendline_values
        touch_indices = np.where(below_trendline[:-1] & ~below_trendline[1:])[0] + 1
        
        if touch_indices.size > 0:
            entry_index = touch_indices[0]
            return data_1min.index[entry_index], data_1min['open'].iloc[entry_index]
        return None, None

    def set_approximate_stop_loss(self, entry_point, data_1min):
        stop_loss = data_1min['low'].loc[:entry_point].tail(5).min()
        return stop_loss

    def calculate_trendline(self, data_5min):
        x = np.arange(len(data_5min))
        y = data_5min['low'].values
        slope, intercept = np.polyfit(x, y, 1)
        return slope, intercept

    def check_entry_condition(self, data_1min, trendline, i):
        x = i
        trendline_value = trendline[0] * x + trendline[1]
        if data_1min['close'].iloc[i-1] <= trendline_value and data_1min['close'].iloc[i] > trendline_value:
            return True
        return False

    def trade_conditions_func(self, df, i, portfolio):
        close = df.loc[i, 'close']
        close5 = df.loc[i, '5min_close']
        spread = df.loc[i, 'spread']
        spread_cost = spread * self.lot_size

        # Spread conversion to currency unit (1 pip = 0.01 yen)
        spread_cost = spread * 0.01 * self.lot_size

        # Profit and loss thresholds
        TAKE_PROFIT = 0.005 * portfolio['entry_price'] if portfolio['entry_price'] else 0
        STOP_LOSS = -0.01 * portfolio['entry_price'] if portfolio['entry_price'] else 0

        # Exit conditions for long position
        if portfolio['position'] == 'long':
            profit = (close - portfolio['entry_price']) - spread_cost
            if profit > TAKE_PROFIT or profit < STOP_LOSS:
                return 'exit_long'

        # Entry conditions for long position
        elif self.check_entry_condition(df, self.calculate_trendline(df), i):
            return 'entry_long'

        else:
            return None

