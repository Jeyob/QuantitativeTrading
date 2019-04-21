import pandas as pd
import numpy as np


class TransformUtils(object):
    """
        A lighweight static class for transforming data in various ways. 

    """

    @classmethod
    def create_price_frame_YAHOO(cls, folder_path=".", filename=None, seperator=',', filetype='csv')->pd.DataFrame:

        # INPUT: takes a path with the data 
        # OUTPUT: outputs a dataframe sorted in ascending order
        try:
            
            IN_SCOPE_COLUMNS = ['Date', 'Open', 'High','Low','Close', 'Adj Close']
            
            if filetype == 'xls':
                price_data = pd.read_excel(folder_path+'/' + filename)
            else:
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
            if price_data['Date'].dtype != np.str:
                price_data['Date'] = price_data['Date'].astype(str)
                price_data['Date'] = price_data['Date'].str.replace('\D','').astype(int)
            else:
                price_data['Date'] = price_data['Date'].str.replace('\D','').astype(int)
            
            #sort rows based on Date in Ascending order. 
            price_data = price_data.sort_values(ascending=True, by=['Date']) 

            #if column(closing prices) is of type np.str, this is likely because the decimal point separate is a ',' rather than '.'  
            if price_data['Closing price'].dtype != np.number:
                price_data['Closing price'] = price_data['Closing price'].str.replace(',','.').astype(float)
            
            return price_data

        except Exception as e:
            print("Unexpected error: {0}".format(e))

