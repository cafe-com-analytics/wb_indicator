import configparser
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

import matplotlib.pyplot as plt
import seaborn as sns   
import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.mlab as m
import pandas_datareader.data as web

from src.data_acquisition.collect_tickers_data import DataCollector
from src.process_data.define_dataframe import unpivot_df


def wb_indicator() -> None:
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
    # indexes_list = sorted(indexes_list.split(','))

    # indexes_selection = st.sidebar.multiselect(f"{market_name} market indexes:", indexes_list)
    indexes_selection = indexes_list

    end_date = date.today()
    start_date = end_date - timedelta(days=3150)
    # start_date = '28/08/2008'

    # start_date = st.sidebar.date_input('Start date', start_date)
    # end_date = st.sidebar.date_input('End date', end_date)

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
        st.markdown(f"""## Selected index(es):\n\n{indexes_selection}\n\nVariation between {start_date} and {end_date}:""")
        data_collector = DataCollector(symbols_list=indexes_selection, start_date=str(start_date), end_date=str(end_date))
        chart_data = data_collector.get_data(data_type="Close")

        chart_data_normalised = chart_data/chart_data.iloc[0]


        # SEABORN AND MATPLOTLIB.
        chart_data_unpivoted = unpivot_df(chart_data_normalised, var_name='index(es)', value_name='return(s)')

        fig, ax = plt.subplots(figsize=(20, 5))
        ax = sns.lineplot(x='Date', y='return(s)', hue='index(es)', data=chart_data_unpivoted, ax=ax)
        plt.grid()
        # X Axis
        plt.xlim(start_date, end_date)
        plt.xticks(rotation=90)
        ax.xaxis.set_major_locator(plt.MultipleLocator(2))
        ax.xaxis.set_major_locator(plt.MaxNLocator(30))
        ax.xaxis.label.set_visible(False)
        # Y Axis
        ax.yaxis.set_major_locator(plt.MultipleLocator(0.01))
        ax.yaxis.set_major_locator(plt.MaxNLocator(10))
        st.pyplot(fig)
        # st.write(chart_data)
        if st.checkbox('Show dataframe'):
            st.write(chart_data_normalised)

        if market_selection == "Brazil":
            # BRAZIL WB INDICATOR
            # Coleta dados do PIB
            pib = DataCollector(start_date='2013-01-01', end_date=date.today().strftime("%Y-%m-%d")).get_gdp()
            # symbols = ['ABEV3.SA', 'ASAI3.SA', 'AZUL4.SA', 'B3SA3.SA', 'BBAS3.SA', 'BBDC3.SA', 'BBDC4.SA', 'BBSE3.SA', 'BEEF3.SA', 'BPAC11.SA', 'BRAP4.SA', 'BRDT3.SA', 'BRFS3.SA', 'BRKM5.SA', 'BRML3.SA', 'BTOW3.SA', 'CCRO3.SA', 'CIEL3.SA', 'CMIG4.SA', 'COGN3.SA', 'CPFE3.SA', 'CPLE6.SA', 'CRFB3.SA', 'CSAN3.SA', 'CSNA3.SA', 'CVCB3.SA', 'CYRE3.SA', 'ECOR3.SA', 'EGIE3.SA', 'ELET3.SA', 'ELET6.SA', 'EMBR3.SA', 'ENBR3.SA', 'ENEV3.SA', 'ENGI11.SA', 'EQTL3.SA', 'EZTC3.SA', 'FLRY3.SA', 'GGBR4.SA', 'GNDI3.SA', 'GOAU4.SA', 'GOLL4.SA', 'HAPV3.SA', 'HGTX3.SA', 'HYPE3.SA', 'IGTA3.SA', 'IRBR3.SA', 'ITSA4.SA', 'ITUB4.SA', 'JBSS3.SA', 'JHSF3.SA', 'KLBN11.SA', 'LAME4.SA', 'LCAM3.SA', 'LREN3.SA', 'MGLU3.SA', 'MRFG3.SA', 'MRVE3.SA', 'MULT3.SA', 'NTCO3.SA', 'PCAR3.SA', 'PETR3.SA', 'PETR4.SA', 'PRIO3.SA', 'QUAL3.SA', 'RADL3.SA', 'RAIL3.SA', 'RENT3.SA', 'SANB11.SA', 'SBSP3.SA', 'SULA11.SA', 'SUZB3.SA', 'TAEE11.SA', 'TIMS3.SA', 'TOTS3.SA', 'UGPA3.SA', 'USIM5.SA', 'VALE3.SA', 'VIVT3.SA', 'VVAR3.SA', 'WEGE3.SA', 'YDUQ3.SA']
            # Coleta dados do valor de echamento das ações
            symbols = config.get('TICKERS', market)
            # a = yf.download(symbols, start="2008-08-28", end="2021-04-02")
            data_collector = DataCollector(symbols_list=symbols, start_date="2013-01-01", end_date=date.today().strftime("%Y-%m-%d"))
            stocks_br = data_collector.get_data()  
            # Unpivot a base baixada da Yahoo Finance
            stocks_br = stocks_br.stack()
            # Nome para a coluna com os tikers das empresas 
            stocks_br.index.set_names('Name', level=1, inplace=True)
            # Tirar as duas primeiras colunas do index
            stocks_br = stocks_br.reset_index(level=['Date', 'Name'])
            # Retira o trecho '.SA' do ticker da empresa
            stocks_br['Name'] = stocks_br['Name'].map(lambda x: str(x)[:-3])
            # Formato da coluna Date
            stocks_br['Date'] = pd.to_datetime(stocks_br['Date'], dayfirst=True)
            # Coleta a quantidade de ações de cada empresa. Arquivo de excel
            qtde_acoes = pd.read_excel('./data/interim/tbl_valor_mercado_010421.xlsx')
            # Cruza a base do preço da ação com a qauntidade de ação
            df = pd.merge(stocks_br, qtde_acoes, on='Name', how='left')
            # Calcula o Market Cap
            df['Marketcap'] = df['qtde_acoes_010421'] * df['Close']
            # Group by por Data e Market Cap
            mktcap_br = df.groupby(['Date']).agg(Marketcap_br=('Marketcap', 'sum'), ).reset_index()
            # Tratamento da unidade do Market Cap
            mktcap_br['Marketcap_br'] = mktcap_br['Marketcap_br'] * 1000
            # Cruzamento com a base de PIB
            mktcap_br['Year'] = mktcap_br['Date'].dt.to_period('Y')
            pib['Year'] = pib['Date'].dt.to_period('Y')
            combined = pd.merge(mktcap_br, pib, on='Year', how='left')
            # Fill NaN PIB 
            combined['PIB'].fillna(method='ffill', inplace=True)
            # Criação do WB Indicator
            combined['Buffett_Indicator'] = combined.Marketcap_br / combined.PIB
            # Filtro de período
            mask = (combined['Date_x'] > '01/01/2013') & (combined['Date_x'] <= date.today().strftime("%d/%m/%Y"))
            combined = combined.loc[mask]
            combined['num_lin'] = np.arange(len(combined))
            # Linha de Tendëncia
            x = combined['num_lin']
            op = combined['Buffett_Indicator']
            coef = np.polyfit(x, op, 1)
            combined['tend'] = coef[0] * x + coef[1]
            # coef = np.polyfit(x, op, 2)
            # combined['tend'] = coef[0] * x ** 2 + coef[1] * x + coef[2]
            stdev = np.std(combined['tend'])
            combined['stdev'] = combined['tend'] + stdev
            combined['2stdev'] = combined['tend'] + stdev + stdev
            combined['stdevneg'] = combined['tend'] - stdev
            combined['2stdevneg'] = combined['tend'] - stdev - stdev
            # PLOT WB Indicator GRAPH
            fig, ax = plt.subplots(figsize=(20, 5))
            ax = sns.lineplot(x='Date_x', y='Buffett_Indicator', data=combined, ax=ax)
            ax = sns.lineplot(x='Date_x', y='tend', data=combined, ax=ax, color = 'gray', alpha = 0.5,  ls="--")
            ax = sns.lineplot(x='Date_x', y='stdev', data=combined, ax=ax, color = 'red', alpha = 0.2)
            ax = sns.lineplot(x='Date_x', y='2stdev', data=combined, ax=ax, color = 'red', alpha = 0.2)
            ax = sns.lineplot(x='Date_x', y='stdevneg', data=combined, ax=ax, color = 'green', alpha = 0.2)
            ax = sns.lineplot(x='Date_x', y='2stdevneg', data=combined, ax=ax, color = 'green', alpha = 0.2)
            plt.grid()
            # X Axis
            # plt.xlim(start_date, end_date)
            plt.xticks(rotation=90)
            ax.xaxis.set_major_locator(plt.MultipleLocator(2))
            ax.xaxis.set_major_locator(plt.MaxNLocator(30))
            ax.xaxis.label.set_visible(False)
            # Y Axis
            ax.yaxis.set_major_locator(plt.MultipleLocator(0.01))
            ax.yaxis.set_major_locator(plt.MaxNLocator(10))
            st.pyplot(fig)
            # st.write(combined)
            # PLOT Market Cap
            fig, ax = plt.subplots(figsize=(20, 5))
            ax = sns.lineplot(x='Date_x', y='Marketcap_br', data=combined, ax=ax)
            plt.grid()
            # X Axis
            # plt.xlim(start_date, end_date)
            plt.xticks(rotation=90)
            ax.xaxis.set_major_locator(plt.MultipleLocator(2))
            ax.xaxis.set_major_locator(plt.MaxNLocator(30))
            ax.xaxis.label.set_visible(False)
            # Y Axis
            ax.yaxis.set_major_locator(plt.MultipleLocator(0.01))
            ax.yaxis.set_major_locator(plt.MaxNLocator(10))
            st.pyplot(fig)
            # st.write(combined)
            # PLOT GDP GRAPH
            fig, ax = plt.subplots(figsize=(20, 5))
            ax = sns.lineplot(x='Date_x', y='PIB', data=combined, ax=ax)
            plt.grid()
            # X Axis
            # plt.xlim(start_date, end_date)
            plt.xticks(rotation=90)
            ax.xaxis.set_major_locator(plt.MultipleLocator(2))
            ax.xaxis.set_major_locator(plt.MaxNLocator(30))
            ax.xaxis.label.set_visible(False)
            # Y Axis
            ax.yaxis.set_major_locator(plt.MultipleLocator(0.01))
            ax.yaxis.set_major_locator(plt.MaxNLocator(10))
            st.pyplot(fig)
            # st.write(combined)
        else:
            # USA WB INDICATOR
            # Date
            end = date.today().strftime("%Y-%m-%d")
            start = '2013-01-01'
            # Puxa GDP e Market Cap
            gdp = web.DataReader('GDP', 'fred', start, end)
            wilshire = web.DataReader('WILL5000PR','fred',start,end)
            # Cruza bases
            combined = pd.concat([gdp,wilshire],axis=1)
            # Get a list of dates available in the GDP dataframe
            gdp_dates = gdp.index.values
            # # Loop through the dgp dates and fill the GDP column in the combined dataframe
            # prev_date = None
            # for date in gdp_dates:
            #     if prev_date == None:
            #         combined.loc[:date,'GDP'] = gdp.loc[date,'GDP']
            #     else:
            #         combined.loc[date_prev:date,'GDP'] = gdp.loc[date_prev,'GDP']
            #     date_prev = date
            # combined.loc[date:,'GDP'] = gdp.loc[date,'GDP']   
            # Fill NaN PIB 
            combined['GDP'].fillna(method='ffill', inplace=True)
            combined['WILL5000PR'].fillna(method='bfill', inplace=True)
            # Buffet indicator
            combined['Buffett_Indicator'] = combined.WILL5000PR / combined.GDP * 100
            # Linha de Tendëncia
            combined['num_lin'] = np.arange(len(combined))
            x = combined['num_lin']
            op = combined['Buffett_Indicator']
            coef = np.polyfit(x, op, 1)
            combined['tend'] = coef[0] * x + coef[1]
            # coef = np.polyfit(x, op, 2)
            # combined['tend'] = coef[0] * x ** 2 + coef[1] * x + coef[2]
            stdev = np.std(combined['tend'])
            combined['stdev'] = combined['tend'] + stdev
            combined['2stdev'] = combined['tend'] + stdev + stdev
            combined['stdevneg'] = combined['tend'] - stdev
            combined['2stdevneg'] = combined['tend'] - stdev - stdev
            # Tira Date do Index
            combined = combined.reset_index(level=['DATE'])
            # PLOT WB Indicator GRAPH
            fig, ax = plt.subplots(figsize=(20, 5))
            ax = sns.lineplot(x='DATE', y='Buffett_Indicator', data=combined, ax=ax)
            ax = sns.lineplot(x='DATE', y='tend', data=combined, ax=ax, color = 'gray', alpha = 0.5,  ls="--")
            ax = sns.lineplot(x='DATE', y='stdev', data=combined, ax=ax, color = 'red', alpha = 0.2)
            ax = sns.lineplot(x='DATE', y='2stdev', data=combined, ax=ax, color = 'red', alpha = 0.2)
            ax = sns.lineplot(x='DATE', y='stdevneg', data=combined, ax=ax, color = 'green', alpha = 0.2)
            ax = sns.lineplot(x='DATE', y='2stdevneg', data=combined, ax=ax, color = 'green', alpha = 0.2)
            plt.grid()
            # X Axis
            # plt.xlim(start_date, end_date)
            plt.xticks(rotation=90)
            ax.xaxis.set_major_locator(plt.MultipleLocator(2))
            ax.xaxis.set_major_locator(plt.MaxNLocator(30))
            ax.xaxis.label.set_visible(False)
            # Y Axis
            ax.yaxis.set_major_locator(plt.MultipleLocator(0.01))
            ax.yaxis.set_major_locator(plt.MaxNLocator(10))
            st.pyplot(fig)
            # st.write(combined)
            # PLOT Market Cap
            fig, ax = plt.subplots(figsize=(20, 5))
            ax = sns.lineplot(x='DATE', y='WILL5000PR', data=combined, ax=ax)
            plt.grid()
            # X Axis
            # plt.xlim(start_date, end_date)
            plt.xticks(rotation=90)
            ax.xaxis.set_major_locator(plt.MultipleLocator(2))
            ax.xaxis.set_major_locator(plt.MaxNLocator(30))
            ax.xaxis.label.set_visible(False)
            # Y Axis
            ax.yaxis.set_major_locator(plt.MultipleLocator(0.01))
            ax.yaxis.set_major_locator(plt.MaxNLocator(10))
            st.pyplot(fig)
            # st.write(combined)
            # PLOT GDP GRAPH
            fig, ax = plt.subplots(figsize=(20, 5))
            ax = sns.lineplot(x='DATE', y='GDP', data=combined, ax=ax)
            plt.grid()
            # X Axis
            # plt.xlim(start_date, end_date)
            plt.xticks(rotation=90)
            ax.xaxis.set_major_locator(plt.MultipleLocator(2))
            ax.xaxis.set_major_locator(plt.MaxNLocator(30))
            ax.xaxis.label.set_visible(False)
            # Y Axis
            ax.yaxis.set_major_locator(plt.MultipleLocator(0.01))
            ax.yaxis.set_major_locator(plt.MaxNLocator(10))
            st.pyplot(fig)