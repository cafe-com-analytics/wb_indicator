import streamlit as st
import numpy as np
import pandas as pd


def main():
    st.title('First test with streamlit')
    st.sidebar.selectbox("Escolha uma opção:", ['Opção 1', 'Opção 2', 'Opção 3'])
    st.header('Tutorial Streamlit - Heroku')
    # st.write('First test with streamlit.')
    st.write(pd.DataFrame({'first column': [1, 2, 3, 4], 'second column': [10, 20, 30, 40]}))

    map_data = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon'])

    st.map(map_data)

    if st.checkbox('Show dataframe'):
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
        st.line_chart(chart_data)


if __name__ == '__main__':
    main()
