import pandas as pd
from scipy.signal import find_peaks
import numpy as np
from datetime import datetime
import logging

class TradingStrategy:
    """
    トレードロジック
    使用データ: 1分足と5分足データを取得（1分足から5分足をリサンプリング）
    1. ５分足のチャート参照
        連続する安値が上昇しているポイントを特定。（極大値・極小値のピーク）
    2. トレンドライン(1)の作成
        上昇する安値のポイントを結ぶ直線を描きます。
        この直線を「トレンドライン(1)」と呼びます。
        ※トレンドラインの定義：（下降トレンドなら極大値の切り下がり、上昇トレンドなら極小値のピークの切り上がり）を結んだもの
        トレンドラインの延長線上に、将来クロスするポイントを見つける
    3. 最新の高値の特定
        ５分足のチャートでの最新の高値を特定します。
    4. 水平線(2)の作成
        最新の高値から水平に直線を引きます。
        この直線を「水平線(2)」と呼びます。
    5. 三角形の形状の作成
        「トレンドライン(1)」と「水平線(2)」の交点を基に、三角形の形状を形成します。
    6. １分足のチャート監視
        価格が「トレンドライン(1)」に触れた後、価格が反転する動き（トレンドラインより下に行った、もしくは触れたあとの上昇を指す）を示した場合、そのポイントで取引を開始（エントリー）します。
    （エントリー条件は、１分足でローソク足が一度、トレンドライン１に触れたあと、再度、１分足の終値がトレンドラインの上で確定したときの、次の始値です）
    7. 利確
        10pipに設定（TODO:将来的にトレールストップを実装する）
    8. ストップロス
        エントリーポイントの直近の安値（極小値）よりも少し下の位置に、損切りのためのストップロス注文を設定
        上昇トレンドラインの起点となっている安値（極小値）のうち、最も近い極小値を直近安値と定義
    """
    def __init__(self, lot_size=10000):
        self.lot_size = lot_size
        self.last_pivots_high = []
        self.last_pivots_low = []
        self.last_trendline = None

    def prepare_data(self, df):
        df["EMA50"] = df["5min_close"].ewm(span=50, adjust=False).mean()
        return df

    def set_approximate_stop_loss(self, entry_point, data_1min):
        stop_loss = data_1min['low'].loc[:entry_point].tail(5).min()
        return stop_loss

    def calculate_trend_line(self, df, direction="high", periods=100, num=2):
        # Use the last N periods for the calculation
        df_last_n = df.tail(periods)
        prices = df_last_n['5min_close'].values

        # Find pivots
        if direction == "high":
            pivots, _ = find_peaks(prices, distance=num)
        else:
            pivots, _ = find_peaks(-prices, distance=num)

        # Check if pivots have changed
        if direction == "high":
            if len(pivots) != len(self.last_pivots_high) or np.any(pivots != self.last_pivots_high):
                self.last_pivots_high = pivots
        elif direction == "low":
            if len(pivots) != len(self.last_pivots_low) or np.any(pivots != self.last_pivots_low):
                self.last_pivots_low = pivots


        # If not enough pivots, return None
        if len(pivots) < num:
            return np.full_like(prices, np.nan)

        # Calculate trend line using least squares method
        y = prices[pivots]
        slope, intercept = np.polyfit(pivots, y, 1)
        trendline = slope * np.arange(len(df_last_n)) + intercept

        # Extend the trendline array to match the original dataframe
        trendline_full = np.full(len(df), np.nan)
        trendline_full[-len(trendline):] = trendline

        return trendline_full

    def check_entry_condition(self, data_1min, trendline, i, price_point):
        trendline_value = trendline[-1]
        # print(f'trendline_value {trendline_value}')
        if price_point == "low":
            condition = data_1min['close'].iloc[i-1] <= trendline_value and data_1min['close'].iloc[i] > trendline_value
        else:
            condition = data_1min['close'].iloc[i-1] >= trendline_value and data_1min['close'].iloc[i] < trendline_value
        return condition


    def trade_conditions_func(self, df, i, portfolio, direction="low"):
        close = df.loc[i, 'close']
        spread = df.loc[i, 'spread']
        spread_cost = spread * 0.01 * self.lot_size

        if portfolio['position'] == 'long':
            TAKE_PROFIT = portfolio['entry_price'] + 0.0010

            profit = (close - portfolio['entry_price']) - spread_cost
            if close >= TAKE_PROFIT or close <= portfolio['STOP_LOSS']:
                portfolio['STOP_LOSS'] = None
                return 'exit_long'

        trendline = self.calculate_trend_line(df, direction)
        if self.check_entry_condition(df, trendline, i, direction):
            if direction == "low":
                portfolio['STOP_LOSS'] = self.last_pivots_low[-1] - 0.0001
            else:
                portfolio['STOP_LOSS'] = self.last_pivots_high[-1] + 0.0001
            return 'entry_long' if direction == "low" else 'entry_short'
        else:
            return None



