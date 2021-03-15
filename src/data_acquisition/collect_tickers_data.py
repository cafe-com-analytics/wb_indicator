from datetime import date
from glob import glob
import os

import pandas as pd
import yfinance as yf


class TickersCollector:

    def __init__(self, market: str = 'br', symbols_list: list = [], qty: int = 10) -> None:
        """This function loads the desirable symbols.
        Args:
            market (str, optional): accepts only 'br' or 'us'. Defaults to 'br'.
            symbols_list (list, optional): list of symbols. Defaults to [].
            qty (int, optional): [description]. Defaults to 100.
        Returns:
            list: list of desirable symbols
        """
        self.market = market
        self.qty = qty

        qty_plus = qty - len(symbols_list)

        symbols = pd.read_csv('./data/interim/lst_stock_symbols.txt', sep=';')
        symbols = symbols.loc[symbols['country'] == market]
        if not symbols_list:
            symbols = symbols.loc[:, 'symbol'].sample(qty_plus, random_state=42).tolist()
            self.symbols_list = symbols
        else:
            symbols = symbols.loc[(~symbols['symbol'].isin(symbols_list)), 'symbol'].sample(qty_plus, random_state=42).tolist()
            symbols.extend(symbols_list)
            self.symbols_list = symbols

    def show_tickers(self) -> list:
        return self.symbols_list

    def add_market(self) -> list:
        symbols_list_w_market = self.symbols_list

        if self.market == 'br':
            symbols_list_w_market.extend(["^BVSP", "^IBX50"])
        else:
            symbols_list_w_market.extend(['SPY', '^IXIC', '^DJI'])

        print(f"Tickers selected: {symbols_list_w_market}")

        return symbols_list_w_market


class DataCollector:

    def __init__(self) -> None:
        pass

    def __verifying_date_format(input_date):
        """This function verify the date format.
        """
        input_date = input_date

        try:
            year = int(input_date[:4])
            month = int(input_date[5:7])
            day = int(input_date[-2:])
            converted_date = str(date(year, month, day))
            correct_date = True
        except ValueError:
            correct_date = False

        return (correct_date, converted_date)



if __name__ == "__main__":
    tickers = TickersCollector(market='br', qty=10)
    tickers.add_market()
    print(tickers.show_tickers())

    # from src.data_acquisition import Market as mk

    # market = ''

    # while market not in ['br', 'us']:
    #     market = input("Which market do you want to evaluate? ['br']/'us': ")
    #     if (len(market.strip()) == 0) or (market.strip() == ''):
    #         market = 'br'
    #         print("Brazilian market was chosed.")
    #     elif market not in ['br', 'us']:
    #         print("Please, follow the instructions.")

    # symbols_list = input("Insert a list of tickers that must be in your analysis as shown in Yahoo! Finance: ")

    # if (len(symbols_list) < 1):
    #     symbols = ''
    # else:
    #     symbols = symbols_list.split(',')
    #     if len(symbols) > 1:
    #         symbols = [item.strip() for item in symbols]
    #         if market == 'br':
    #             symbols = [item+'.SA' for item in symbols]

    # try:
    #     qty = int(input("Insert the quantity of stocks: "))
    #     if not qty:
    #         raise ValueError('Empty input')
    # except ValueError as e:
    #     print(e)
    #     print("Qty was not inserted. Default = 50.")
    #     qty = 50

    # symbols = mk.load_stock_list(market=market, symbols_list=symbols, qty=qty)

    # date_start = input("Insert the INITIAL date in the following format ('YYYY-MM-DD') ['2020-01-01']: ")
    # if date_start == '':
    #     date_start = '2020-01-01'
    # else:
    #     date_start = mk.__verifying_date_format(date_start)[1]

    # date_end = input("Insert the ENDING date in the following format ('YYYY-MM-DD') [today]: ")
    # if date_end == '':
    #     date_end = str(date.today())
    # else:
    #     date_end = mk.__verifying_date_format(date_end)[1]

    # if not os.path.exists('data/raw'):
    #     os.mkdir('data/raw')

    # lst_delist = []
    # ok = nok = 0

    # for symbol in symbols:
    #     if not os.path.exists(f"data/raw/{market}_{symbol}.csv"):
    #         data = yf.download(symbol, start=date_start, end=date_end)
    #         if data.size > 0:
    #             data.to_csv(f"data/raw/{market}_{symbol}.csv")
    #             ok += 1
    #         else:
    #             print("Not saving...")
    #             nok += 1
    #             lst_delist.append(symbol)

    # for symbol in symbols:
    #     try:
    #         s = open(f"data/raw/{market}_{symbol}.csv").readlines()
    #         if len(s) < 10:
    #             os.system(f"rm data/raw/{market}_{symbol}.csv")
    #     except:
    #         print(f"{market}_{symbol}.csv does not exist.")
    #         continue

    # lst_delist = pd.DataFrame(lst_delist)
    # lst_delist.to_csv('./data/interim/lst_delist.txt', index=False)

    # files = glob('data/raw/*.csv')

    # full_df = None
    # for file in files:
    #     df = pd.read_csv(file)
    #     symbol = file.split('/')[-1].split('\\')[-1].split('.')[0].split('_')[1]
    #     df['Name'] = symbol

    #     if full_df is None:
    #         full_df = df
    #     else:
    #         full_df = full_df.append(df, ignore_index=True)

    # full_df = full_df[['Date', 'Name', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

    # today_var = str(date.today()).replace('-', '_')
    # full_df.to_parquet(f'data/interim/data_acquired_{today_var}.pqt', index=False)

    # df_close_prices = pd.pivot_table(full_df, values='Close', columns=['Name'], index=['Date'])
    # df_close_prices.to_parquet(f'data/interim/data_acquired_close_{today_var}.pqt', index=True)
