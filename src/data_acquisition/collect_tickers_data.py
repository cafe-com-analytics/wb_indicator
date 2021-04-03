import configparser
from datetime import date, timedelta

import pandas as pd
import yfinance as yf


def _verifying_date_format(input_date):
    """This function verify the date format."""
    input_date = input_date

    try:
        year = int(input_date[:4])
        month = int(input_date[5:7])
        day = int(input_date[-2:])
        converted_date = date(year, month, day)
        correct_date = True
    except ValueError:
        correct_date = converted_date = date(2015, 1, 1)

    return (correct_date, converted_date)


class DataCollector:

    def __init__(self, *, symbols_list: list = None, start_date: str, end_date: str) -> None:
        self.symbols_list = symbols_list
        # TODO: NECESSÁRIO INCLUIR UM MÉTODO QUE VALIDE A LISTA DE SÍMBOLOS INSERIDA.
        self.start_date = _verifying_date_format(start_date)[-1]
        self.end_date = _verifying_date_format(end_date)[-1] + timedelta(days=1)
        # TODO: VERIFICAR A NECESSIDADE DE INCLUIR VALIDAÇÕES DE DATA E ALTERAÇÃO CASO DATA FORNECIDA NÃO SEJA OK.

    def get_data(self, *, data_type: str = None) -> pd.DataFrame:
        """get_data returns a pandas.DataFrame of the chosen data_type.
        Args:
            data_type (str): "Adj Close", "Close", "High", "Low", "Open", or "Volume"
        Returns:
            DataFrame: with the data_type time series
        """
        # FIXME: TROCAR A CRIAÇÃO DE ARQUIVO POR ADICIONAR CONEXÃO COM BANCO DE DADOS.
        # TODO: POR ENQUANTO, ESTOU TESTANDO SOMENTE COM O "close", porém, devemos deixar que o usuário escolha o tipo de dado (Opne, Close...).
        data = yf.download(self.symbols_list, start=self.start_date, end=self.end_date)
        if data_type:
            data = data[data_type]

        return data

    def get_gdp(codigo_bcb: str = '1207') -> pd.DataFrame:
        url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.1207/dados?formato=json'
        df = pd.read_json(url)
        df['Date'] = pd.to_datetime(df['data'], dayfirst=True)
        df.drop(['data'], axis=1, inplace=True)
        df.rename(columns={'valor': 'PIB'}, inplace=True)

        return df

    def get_tickers_set(self, *, market: str = 'br', qty: int = 10) -> pd.DataFrame:
        """[summary]
        Args:
            market (str, optional): [description]. Defaults to 'br'.
            symbols_list (list, optional): [description]. Defaults to [].
            qty (int, optional): [description]. Defaults to 10.
        Returns:
            pd.DataFrame: [description]
        """
        symbols_list = self.symbols_list

        config = configparser.ConfigParser()
        config.read('config.ini')
        symbols = config.get('TICKERS', market)
        symbols = sorted(symbols.split(','))
        qty_plus = max([qty - len(symbols_list), 0])

        if not symbols_list:
            symbols = symbols.loc[:, 'symbol'].sample(qty_plus, random_state=42).tolist()
        else:
            symbols = symbols.loc[(~symbols['symbol'].isin(symbols_list)), 'symbol'].sample(qty_plus, random_state=42).tolist()
            symbols.extend(symbols_list)

        return symbols

    def add_market(self) -> list:
        symbols_list_w_market = self.symbols_list

        if self.market == 'br':
            symbols_list_w_market.extend(["^BVSP", "^IBX50"])
        else:
            symbols_list_w_market.extend(['SPY', '^IXIC', '^DJI'])

        return symbols_list_w_market


if __name__ == "__main__":
    data_collector = DataCollector(symbols_list=["ITUB4.SA"], start_date='2021-01-01', end_date='2021-03-01')
    print(data_collector.get_data(data_type='Close'))
