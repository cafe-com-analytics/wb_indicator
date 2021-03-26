import configparser
from datetime import date, timedelta

import streamlit as st

from src.data_acquisition.collect_tickers_data import TickersCollector, DataCollector


def main():
    # Reading config file with tickers.
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Sidebar section:
    market_selection = st.sidebar.radio("Escolha uma opção:", ["Brasil", "EUA"])

    if market_selection == "Brasil":
        market = "br"
    else:
        market = "us"

    tickers_list = config.get('TICKERS', market)
    tickers_list = sorted(tickers_list.split(','))

    tickers_selection = st.sidebar.multiselect("Tickers:", tickers_list)

    end_date = date.today()
    start_date = end_date + timedelta(days=-180)

    start_date = st.sidebar.date_input('Start date', start_date)
    end_date = st.sidebar.date_input('End date', end_date)

    if start_date < end_date:
        st.sidebar.success(f'Start date: {start_date}\n\nEnd date: {end_date}')
    else:
        st.sidebar.error('Error: End date must fall after start date.')

    # Principal section or visualization section:
    st.title('WB Indicator')
    st.header('Indice do mercado selecionado')
    st.write('Retorno ao longo do tempo:')

    symbols_list = []
    symbols_list.extend(tickers_selection)

    tickers = TickersCollector(market=market, symbols_list=symbols_list, qty=0)
    tickers.add_market()
    lst_tickers = tickers.show_tickers()

    data_collector = DataCollector(symbols_list=lst_tickers, start_date=str(start_date), end_date=str(end_date))

    chart_data = data_collector.get_data(data_type="Close")
    chart_data_normalised = chart_data/chart_data.iloc[0]
    st.line_chart(chart_data_normalised)
    #  TODO: TRY TO USE SEABORN AND MATPLOTLIB.

    if st.checkbox('Show dataframe'):
        st.write(chart_data_normalised)


if __name__ == '__main__':
    main()
