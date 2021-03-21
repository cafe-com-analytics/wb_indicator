# import numpy as np
# import pandas as pd
import streamlit as st

from src.data_acquisition.collect_tickers_data import TickersCollector, DataCollector


def main():
    st.title('First test with streamlit')
    st.sidebar.selectbox("Escolha uma opção:", ['Opção 1', 'Opção 2', 'Opção 3'])
    st.header('Tutorial Streamlit - Heroku')
    st.write('First test with streamlit.')
    # st.write(pd.DataFrame({'first column': [1, 2, 3, 4], 'second column': [10, 20, 30, 40]}))

    # map_data = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon'])

    # st.map(map_data)

    if st.checkbox('Show dataframe'):
        tickers = TickersCollector(market='br', qty=10)
        tickers.add_market()
        lst_tickers = tickers.show_tickers()
        data_collector = DataCollector(symbols_list=lst_tickers, start_date='2021-01-01', end_date='2021-03-01')

        chart_data = data_collector.get_data(data_type="Close")
        st.line_chart(chart_data)

        st.write(chart_data)


if __name__ == '__main__':
    main()
