# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401

# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IStrategy, IntParameter)
from pandas_ta.utils import data

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import pandas_ta as pd_ta 

 # AL PARECER DA MEJOR RENDIMIENTO SIN USAR LA EMA DE 200 PERIODOS

class Super3(IStrategy):
    """
    This is a strategy template to get you started.
    More information in https://www.freqtrade.io/en/latest/strategy-customization/

    You can:
        :return: a Dataframe with all mandatory indicators for the strategies
    - Rename the class name (Do not forget to update class_name)
    - Add any methods you want to build your strategy
    - Add any lib you need to build your strategy

    You must keep:
    - the lib in the section "Do not remove these libs"
    - the methods: populate_indicators, populate_buy_trend, populate_sell_trend
    You should keep:
    - timeframe, minimal_roi, stoploss, trailing_*
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "0":  100
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.1

    # Trailing stoploss
    trailing_stop = False
    # trailing_only_offset_is_reached = False
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.0  # Disabled / not configured

    # Optimal timeframe for the strategy.
    timeframe = '1d'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    # Optional order type mapping.
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc'
    }
    
    plot_config = {
        # Main plot indicators (Moving averages, ...)
        'main_plot': {
            'ST_long':{'color': 'green'},
            'ST_short':{'color': 'red'},
            'ST_long2':{'color': 'green'},
            'ST_short2':{'color': 'red'},
            'ST_long3':{'color': 'green'},
            'ST_short3':{'color': 'red'},
            'bb_upperband':{'color': 'grey'},
            'bb_middleband':{'color': 'red'},
            'bb_lowerband':{'color': 'grey'},
            'ema200':{'color':'yellow'}
           
        },
        'subplots': {
            # Subplots - each dict defines one additional plot
        
            "ADX": {
                'adx': {'color': 'red'},
                'fuerza': {'color':'blue'}
               
            }
        }
    }
  
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

         #ADx

          dataframe['adx'] = ta.ADX(dataframe)
          dataframe['fuerza'] = 23
          



        # Ema

          dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)

        
        #Supertrend

          periodo = 11
          atr_multiplicador = 2.0
    
          dataframe['ST_long'] = pd_ta.supertrend(dataframe['high'], dataframe['low'], dataframe['close'], length=periodo,
                                                  multiplier=atr_multiplicador)[f'SUPERTl_{periodo}_{atr_multiplicador}']

          dataframe['ST_short'] = pd_ta.supertrend(dataframe['high'], dataframe['low'], dataframe['close'], length=periodo,
                                                  multiplier=atr_multiplicador)[f'SUPERTs_{periodo}_{atr_multiplicador}']
          periodo2 = 12
          atr_multiplicador2 = 3.0
    
          dataframe['ST_long2'] = pd_ta.supertrend(dataframe['high'], dataframe['low'], dataframe['close'], length=periodo2,
                                                  multiplier=atr_multiplicador2)[f'SUPERTl_{periodo2}_{atr_multiplicador2}']

          dataframe['ST_short2'] = pd_ta.supertrend(dataframe['high'], dataframe['low'], dataframe['close'], length=periodo2,
                                                  multiplier=atr_multiplicador2)[f'SUPERTs_{periodo2}_{atr_multiplicador2}']
          periodo3 = 7
          atr_multiplicador3 = 3.0
    
          dataframe['ST_long3'] = pd_ta.supertrend(dataframe['high'], dataframe['low'], dataframe['close'], length=periodo3,
                                                  multiplier=atr_multiplicador3)[f'SUPERTl_{periodo3}_{atr_multiplicador3}']

          dataframe['ST_short3'] = pd_ta.supertrend(dataframe['high'], dataframe['low'], dataframe['close'], length=periodo3,
                                                  multiplier=atr_multiplicador3)[f'SUPERTs_{periodo3}_{atr_multiplicador3}']


         #Bollinger

          bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=1.5)
          dataframe['bb_lowerband'] = bollinger['lower']
          dataframe['bb_middleband'] = bollinger['mid']
          dataframe['bb_upperband'] = bollinger['upper']
          dataframe["bb_percent"] = (
          (dataframe["close"] - dataframe["bb_lowerband"]) /
            (dataframe["bb_upperband"] - dataframe["bb_lowerband"])
           )
          dataframe["bb_width"] = (
            (dataframe["bb_upperband"] - dataframe["bb_lowerband"]) / dataframe["bb_middleband"]
           )  

          return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    
        dataframe.loc[
            (
                (dataframe['ST_long'] < dataframe['close']) & 
                (dataframe['ST_long2'] < dataframe['close']) & 
                (dataframe['ST_long3'] < dataframe['close']) & 
                # (dataframe['ema200'] < dataframe['close']) & 
               
                # (dataframe['adx'] > 23) &
                # (dataframe['close'] <  dataframe['bb_upperband']) & 

                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
 
        dataframe.loc[
            (   
                (dataframe['ST_short'] > dataframe['close']) & 
                (dataframe['ST_short2'] > dataframe['close']) & 
                (dataframe['ST_short3'] > dataframe['close']) & 
              (dataframe['close'] >=  dataframe['bb_middleband'] ) &
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            'sell'] = 1
        return dataframe
    