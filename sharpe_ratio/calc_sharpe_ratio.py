import pandas as pd
import numpy as np
from decimal import Decimal

def ANNUALISED_AVG_RISK_FREE_RATE() -> float: 
    return 0.04 #dummy value assuming 4% annualised risk free interest rate

def NUM_TRADING_PERIODS_ANNUALLY() -> float:
    return 252.0

def create_price_frame_NASDAQ(folder_path=".", filename=None):

    # INPUT: takes a path with the data 
    # OUTPUT: outputs the sharp ratio which is a float number
    try:
        
        price_data = pd.read_csv(folder_path + '/' + filename, sep=';')
        #Remove all columns in data expect for Date, Opening price, High price, Low price, Closing price    
        price_data.drop(['Unnamed: 11','Bid','Ask','Low price','Average price', 'Total volume', 'Turnover', 'Trades'], inplace=True, axis=1)
        
        price_data['Date'] = price_data['Date'].str.replace('\D','').astype(int)
        
        price_data = price_data.sort_values(ascending=True, by=['Date'])

        price_data['Closing price'] = price_data['Closing price'].str.replace(',','.').astype(float)
        
        return price_data

    except Exception as e:
        print("Unexpected error: {0}".format(e))

def create_price_frame_YAHOO(folder_path=".", filename=None):

    # INPUT: takes a path with the data 
    # OUTPUT: outputs the sharp ratio which is a float number
    try:
        
        price_data = pd.read_csv(folder_path + '/' + filename, sep=';')
        #Remove all columns in data expect for Date, Opening price, High price, Low price, Closing price    
        #price_data.drop(['Unnamed: 11','Bid','Ask','Low price','Average price', 'Total volume', 'Turnover', 'Trades'], inplace=True, axis=1)
        
        price_data.columns = ['Date', 'Opening price', 'High price', 'Low price', 'Closing price']

        price_data['Date'] = price_data['Date'].str.replace('\D','').astype(int)
        
        price_data = price_data.sort_values(ascending=True, by=['Date'])

        price_data['Closing price'] = price_data['Closing price'].str.replace(',','.').astype(float)
        
        return price_data

    except Exception as e:
        print("Unexpected error: {0}".format(e))


def calc_sharp_ratio(df_prices: pd.DataFrame):
    #Input: a dataframe with the columns Date, Opening price, High price, Low price, Closing price
    #Output: sharp_ratio: double

    cls = np.array(df_prices['Closing price'])

    daily_returns = (cls[1:] - cls[:len(cls)-1])/cls[:len(cls)-1]

    excess_daily_returns = daily_returns - ANNUALISED_AVG_RISK_FREE_RATE()/NUM_TRADING_PERIODS_ANNUALLY()

    sharp_ratio = (np.sqrt(252) * np.mean(excess_daily_returns))/np.std(excess_daily_returns)
    
    return sharp_ratio


#price_frame = create_price_frame_NASDAQ(filename='ERIC-B-2018-01-01-2019-01-01.csv')
price_frame = create_price_frame_YAHOO(filename='IGE.csv')
sharp_ratio = calc_sharp_ratio(price_frame)

print("Sharp ratio: {0}".format(sharp_ratio))