import pandas as pd
import numpy as np
from decimal import Decimal

def ANNUALISED_AVG_RISK_FREE_RATE() -> float: 
    return 0.04 #dummy value assuming 4% annualised risk free interest rate

def NUM_TRADING_PERIODS_ANNUALLY() -> int:
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

def create_price_frame_YAHOO(folder_path=".", filename=None, seperator=',')->pd.DataFrame:

    # INPUT: takes a path with the data 
    # OUTPUT: outputs the sharp ratio which is a float number
    try:
        
        IN_SCOPE_COLUMNS = ['Date', 'Open', 'High','Low','Close', 'Adj Close']
        
        price_data = pd.read_csv(folder_path + '/' + filename, sep=seperator)
        
        #drop all columns that we dont need
        for col in price_data.columns:
            if col not in IN_SCOPE_COLUMNS:
                price_data.drop([col], inplace=True, axis=1)
        
        if 'Close' in price_data.columns and 'Adj Close' in price_data.columns:
            price_data.drop(['Close'], inplace=True, axis=1) #prefer Adjusted close

        #change names to columns 
        price_data.columns = ['Date', 'Opening price', 'High price', 'Low price', 'Closing price']

        #Remove '-' from Date string -> YYYYMMDD
        price_data['Date'] = price_data['Date'].str.replace('\D','').astype(int)
        
        #sort rows based on Date in Ascending order. 
        price_data = price_data.sort_values(ascending=True, by=['Date']) 

        #if column(closing prices) is of type np.str, this is likely because the decimal point separate is a ',' rather than '.'  
        if price_data['Closing price'].dtype != np.number:
            price_data['Closing price'] = price_data['Closing price'].str.replace(',','.').astype(float)
        
        return price_data

    except Exception as e:
        print("Unexpected error: {0}".format(e))


def calc_sharp_ratio(df_prices: pd.DataFrame):
    #Input: a dataframe with the columns: Date, Opening price, High price, Low price, Closing price
    #Output: sharp_ratio: double

    cls = np.array(df_prices['Closing price'])

    daily_returns = (cls[1:] - cls[:len(cls)-1])/cls[:len(cls)-1]

    excess_daily_returns = daily_returns - ANNUALISED_AVG_RISK_FREE_RATE()/NUM_TRADING_PERIODS_ANNUALLY()

    sharp_ratio = (np.sqrt(252) * np.mean(excess_daily_returns))/np.std(excess_daily_returns)
    
    return sharp_ratio

def calc_sharp_ratio_market_neutral(df_prices1: pd.DataFrame, df_prices2: pd.DataFrame) -> float:

    cls1 = np.array(df_prices1['Closing price']) #IGE price frame
    cls2 = np.array(df_prices2['Closing price']) #SPY price frame

    daily_returns1 = (cls1[1:] - cls1[:len(cls1)-1])/cls1[:len(cls1)-1]
    daily_returns2 = (cls2[1:] - cls2[:len(cls2)-1])/cls2[:len(cls2)-1]

    #because we now have twice as much capital we must divide by two
    netret = (daily_returns1 - daily_returns2)/2

    excess_daily_returns = netret #we do not substract the risk-free rate from the returns as the short position essentially financies the purchase of the long position

    sharp_ratio = (np.sqrt(NUM_TRADING_PERIODS_ANNUALLY()) * np.mean(excess_daily_returns))/np.std(excess_daily_returns)
     
    return sharp_ratio

#price_frame = create_price_frame_NASDAQ(filename='ERIC-B-2018-01-01-2019-01-01.csv')
price_frame_IGE = create_price_frame_YAHOO(folder_path="./source_data", filename='IGE.csv', seperator=',')
price_frame_SPY = create_price_frame_YAHOO(folder_path="./source_data", filename='SPY_MOD_ADJ.csv', seperator=',')

assert len(price_frame_IGE) == len(price_frame_SPY)

sharp_ratio = calc_sharp_ratio(price_frame_IGE)

print("\nSharp ratio (long-only): {0}\n".format(sharp_ratio))

sharp_ratio_market_neutral = calc_sharp_ratio_market_neutral(price_frame_IGE, price_frame_SPY)

print("Sharp ratio (market neutral): {0}\n".format(sharp_ratio_market_neutral))
