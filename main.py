# import numpy as np
# import pandas as pd
import streamlit as st

from src.data_acquisition.collect_tickers_data import TickersCollector, DataCollector


def main():
    st.title('WB Indicator')
    st.sidebar.selectbox("Escolha uma opção:", ['Brasil', 'EUA'])
    st.header('Ticker(s) e índice do mercado selecionado')
    st.write('Índices ao longo do tempo:')
    
    # st.write(pd.DataFrame({'first column': [1, 2, 3, 4], 'second column': [10, 20, 30, 40]}))
    # map_data = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon'])
    # st.map(map_data)

    tickers = TickersCollector(market='br', symbols_list=['ITUB4.SA'], qty=2)
    tickers.add_market()
    lst_tickers = tickers.show_tickers()
    data_collector = DataCollector(symbols_list=lst_tickers, start_date='2018-03-21', end_date='2021-03-21')

    chart_data = data_collector.get_data(data_type="Close")
    chart_data_normalised = chart_data/chart_data.iloc[0]
    st.line_chart(chart_data_normalised)

    if st.checkbox('Show dataframe'):
        st.write(chart_data_normalised)


if __name__ == '__main__':
    main()
