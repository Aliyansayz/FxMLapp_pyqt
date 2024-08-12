from twelvedata import TDClient

# Initialize client - apikey parameter is requiered
td = TDClient(apikey="YOUR_API_KEY_HERE")

# Construct the necessary time series
ts = td.time_series(
    symbol="AAPL",
    interval="1min",
    outputsize=10,
    timezone="America/New_York",
)

# Returns pandas.DataFrame
ts.as_pandas()




from twelvedata import TDClient

td = TDClient(apikey="YOUR_API_KEY_HERE")
ts = td.time_series(
    symbol="ETH/BTC",
    exchange="Huobi",
    interval="5min",
    outputsize=22,
    timezone="America/New_York",
)

# Returns: OHLC, BBANDS(close, 20, 2, EMA), PLUS_DI(9), WMA(20), WMA(40)
ts.with_bbands(ma_type="EMA").with_plus_di().with_wma(time_period=20).with_wma(time_period=40).as_pandas()

# Returns: STOCH(14, 1, 3, SMA, SMA), TSF(close, 9)
ts.without_ohlc().with_stoch().with_tsf().as_json()


# https://github.com/twelvedata/twelvedata-python

