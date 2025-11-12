def get_option_info(ticker,api,call=True):
    import yfinance as yf

    ticker = yf.Ticker(ticker)
    S0 = ticker.history(period="1d")["Close"].iloc[-1]
    expirations = ticker.options

    # Picking the nearest expiry one
    expiry = expirations[0]

    chain = ticker.option_chain(expiry)
    if call:
        options = chain.calls
    else:
        options = chain.puts

    mid_price=(options["ask"].iloc[0]+options["bid"].iloc[0])/2
    bid=options["bid"].iloc[0]
    ask=options["ask"].iloc[0]

    K = options['strike'].iloc[0]

    from fredapi import Fred
    fred = Fred(api_key=api)  # get one from https://fred.stlouisfed.org/
    r_series = fred.get_series_latest_release("DGS1MO") / 100  # 1-month Treasury yield
    r=r_series.iloc[-1]

    import numpy as np

    data = ticker.history(period="1y")
    returns = np.log(data["Close"] / data["Close"].shift(1))
    sigma = np.std(returns.dropna()) * np.sqrt(252)

    import datetime as dt

    today = dt.date.today()
    expiry_date = dt.datetime.strptime(expiry, "%Y-%m-%d").date()
    T = (expiry_date - today).days / 365
    
    return S0,K,r,sigma,T,mid_price,bid,ask
