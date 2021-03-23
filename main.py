# import numpy as np
# import pandas as pd
from datetime import date, timedelta
import streamlit as st

from src.data_acquisition.collect_tickers_data import TickersCollector, DataCollector


def main():
    st.title('WB Indicator')
    # st.sidebar.selectbox("Escolha uma opção:", ['Brasil', 'EUA'])
    market_selection = st.sidebar.radio("Escolha uma opção:", ["Brasil", "EUA"])

    # IMPROVEMENT: Logo abaixo, deixamos uma opção ao radio buttom acima. Talvez seja legal com ações.
    # st.sidebar.multiselect("Escolha uma opção:", ["Brasil", "EUA"])

    if market_selection == "Brasil":
        market = "br"
    else:
        market = "us"

    st.header('Indice do mercado selecionado')
    st.write('Retorno ao longo do tempo:')

    # st.write(pd.DataFrame({'first column': [1, 2, 3, 4], 'second column': [10, 20, 30, 40]}))
    # map_data = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon'])
    # st.map(map_data)

    tickers = TickersCollector(market=market, symbols_list=[], qty=0)
    tickers.add_market()
    lst_tickers = tickers.show_tickers()

    end_date = date.today()
    start_date = end_date + timedelta(days=-180)

    start_date = st.sidebar.date_input('Start date', start_date)
    end_date = st.sidebar.date_input('End date', end_date)

    if start_date < end_date:
        st.sidebar.success(f'Start date: {start_date}\n\nEnd date: {end_date}')
    else:
        st.sidebar.error('Error: End date must fall after start date.')

    data_collector = DataCollector(symbols_list=lst_tickers, start_date=str(start_date), end_date=str(end_date))

    chart_data = data_collector.get_data(data_type="Close")
    chart_data_normalised = chart_data/chart_data.iloc[0]
    st.line_chart(chart_data_normalised)

    if st.checkbox('Show dataframe'):
        st.write(chart_data_normalised)


if __name__ == '__main__':
    main()
