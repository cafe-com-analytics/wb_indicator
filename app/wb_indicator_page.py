import configparser
from datetime import date, timedelta

from bokeh.plotting import figure, show
# import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns
import streamlit as st

from src.data_acquisition.collect_tickers_data import DataCollector


def unpivot_df(df: pd.DataFrame, var_name: str = 'index(es)', value_name: str = 'return(s)') -> pd.DataFrame:
    df = df.reset_index()
    df = df.melt('Date', var_name=var_name, value_name=value_name)
    df.dropna(how='any', inplace=True)
    return df


def wb_indicator():
    # Reading config file with tickers.
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Sidebar section:
    market_selection = st.sidebar.radio("Choose a market:", ["Brazil", "USA"])

    if market_selection == "Brazil":
        market = "br"
        market_name = "Brazilian"
    else:
        market = "us"
        market_name = "American"

    indexes_list = config.get('MARKET', market)
    indexes_list = sorted(indexes_list.split(','))

    indexes_selection = st.sidebar.multiselect(f"{market_name} market indexes:", indexes_list)

    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    start_date = st.sidebar.date_input('Start date', start_date)
    end_date = st.sidebar.date_input('End date', end_date)

    if start_date < end_date:
        st.sidebar.info(f"""Start date: {start_date}\n\nEnd date: {end_date}""")
    else:
        st.sidebar.error('Error: End date must fall after start date.')

    # Principal section or visualization section:
    st.markdown('# Warren Buffet Indicator')
    symbols_list = []
    symbols_list.extend(indexes_selection)

    if len(indexes_selection) <= 0:
        st.markdown("""## Nothing to show yet.\n\nPlease use the sidebar options.""")
    else:
        st.markdown(f"""## Selected index(es): {indexes_selection}\n\nVariation between {start_date} and {end_date}:""")
        data_collector = DataCollector(symbols_list=indexes_selection, start_date=str(start_date), end_date=str(end_date))
        chart_data = data_collector.get_data(data_type="Close")

        chart_data_normalised = chart_data/chart_data.iloc[0]
        # st.line_chart(chart_data_normalised)

        # TODO: TRY TO USE SEABORN AND MATPLOTLIB.
        chart_data_unpivoted = unpivot_df(chart_data_normalised, var_name='index(es)', value_name='return(s)')
        p = figure(title="WB Indicator", x_axis_label='Date', y_axis_label='WB Indicator [marketcap/gdp]')
        p.line(chart_data_unpivoted["Date"], chart_data_unpivoted.iloc[:, -1], legend_label="Temp", line_width=2)
        show(p)

        # fig, ax = plt.subplots(figsize=(20, 5))
        # ax = sns.lineplot(x='Date', y='return(s)', hue='index(es)', data=chart_data_unpivoted, ax=ax)
        # plt.xlim(start_date, end_date)
        # st.pyplot(fig)

        if st.checkbox('Show dataframe'):
            st.write(chart_data_normalised)
