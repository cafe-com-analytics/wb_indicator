import streamlit as st

from app.wb_indicator_page import wb_indicator
from app.tickers_page import tickers_indicator

st.set_page_config(page_title="WB Indicator", page_icon=":chart_with_upwards_trend:", layout='wide', initial_sidebar_state='auto')


def main():
    # Sidebar section:
    # page_selection = st.sidebar.radio("Select one option:", ["WB Indicator", "Tickers"])

    # if page_selection == "WB Indicator":
    #     wb_indicator()
    # elif page_selection == "Tickers":
    #     tickers_indicator()

    tickers_indicator()


if __name__ == '__main__':
    main()
