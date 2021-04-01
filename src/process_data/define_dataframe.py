import pandas as pd


def unpivot_df(df: pd.DataFrame, var_name: str = 'index(es)', value_name: str = 'return(s)') -> pd.DataFrame:
    df = df.reset_index()
    df = df.melt('Date', var_name=var_name, value_name=value_name)
    df.dropna(how='any', inplace=True)
    return df

