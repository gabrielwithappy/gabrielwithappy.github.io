import numpy as np
import pandas as pd
import FinanceDataReader as fdr
from module.open_ecos_reader.ECOSReader import ECOSReader
import os

def load_korea_nsi(dstfile, api_key):
    print('load_korea_nsi')
    reader = ECOSReader(api_key)
    start_date = (pd.Timestamp.now() - pd.DateOffset(years=1)).strftime("%Y%m%d")
    end_date = (pd.Timestamp.now()).strftime("%Y%m%d")
    nsi_df = reader.statiscic_search(start_date, end_date, '521Y001', 'D')
    nsi_df['DATA_VALUE'] = nsi_df['DATA_VALUE'].astype('float')
    nsi_df.rename(columns = {'DATA_VALUE' : 'NSI'}, inplace=True)
    nsi_df['Date'] = pd.to_datetime(nsi_df['TIME'])
    nsi_df = nsi_df.set_index('Date')
    path = "../website/dashboard_blog/posts/kospi_monthly_returns/"
    filename = 'result_kospi_monthly_returns.csv'
    kospi_df = pd.read_csv(os.path.join(path, filename))
    kospi_df['Date'] = pd.to_datetime(kospi_df['Date'])
    kospi_df = kospi_df.set_index('Date')
    df = pd.merge(nsi_df, kospi_df, how='right', on='Date')
    df.to_csv(dstfile)

def monthly_returns(name, dstfile, key):
    print("monthly_returns()")
    df = fdr.DataReader(name, start=str(pd.Timestamp.now().year - 5))

    start_date = (pd.Timestamp.now() - pd.DateOffset(days=5)).strftime("%Y%m%d")
    end_date = (pd.Timestamp.now()).strftime("%Y%m%d")

    reader = ECOSReader(key)
    df_temp = reader.statiscic_search(start_date, end_date, '817Y002', 'D') # 금리 daily
    df_temp['DATA_VALUE'] = df_temp['DATA_VALUE'].astype('float')
    df_temp['TIME'] = pd.to_datetime(df_temp['TIME'])
    df_temp = df_temp.set_index('TIME')
    rate = df_temp[df_temp['ITEM_NAME1'] == '국고채(3년)']['DATA_VALUE'].to_list()[-1]
    monthly_rate = np.power(rate, 1/12)-1
    df['국고채(3년)'] = rate
    df['국고채(3년)-월복리'] = monthly_rate

    df.to_csv(dstfile)


def make_kospi_MDD(dstfile, key):
    print("make_kospi_MDD")
    kospi_df = fdr.DataReader('KS11', start=str(pd.Timestamp.now().year - 5) )

    window = 252
    kospi_df['Peak'] = kospi_df['Adj Close'].cummax()
    kospi_df['DD'] = kospi_df['Adj Close']/kospi_df['Peak'] - 1
    window = 252
    kospi_df['MDD'] = kospi_df['DD'].rolling(window, min_periods=1).min()
    kospi_df['MDD(6개월평균)'] = kospi_df['MDD'].rolling(30*6, min_periods=1).mean()
    kospi_df.to_csv(dstfile, encoding='cp949')

def make_sp500_MDD(dstfile, key):
    print("make_s&p500_mdd")
    spy_df = fdr.DataReader('US500', start=str(pd.Timestamp.now().year - 5) )

    window = 252
    spy_df['Peak'] = spy_df['Adj Close'].cummax()
    spy_df['DD'] = spy_df['Adj Close']/spy_df['Peak'] - 1
    window = 252
    spy_df['MDD'] = spy_df['DD'].rolling(window, min_periods=1).min()
    spy_df['MDD(6개월평균)'] = spy_df['MDD'].rolling(30*6, min_periods=1).mean()
    spy_df.to_csv(dstfile, encoding='cp949')





