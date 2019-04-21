import TransformUtils as turil
import pandas as pd
import numpy as np
from scipy import stats as scs
import statsmodels.api as sms
import matplotlib.pyplot as plt

gdx_df = turil.TransformUtils.create_price_frame_YAHOO(folder_path='./source_data', filename='GDX.xls', filetype='xls') 
gld_df = turil.TransformUtils.create_price_frame_YAHOO(folder_path='./source_data', filename='GLD.xls', filetype='xls')

#Merge the two dataframes on the intersection data
com_df = pd.merge(gld_df, gdx_df, on='Date', suffixes=('_GLD', '_GDX'))

# split the historic data in a training and testset 
trainset = np.array(range(252)) #creates array indices 0 to 251
testset = np.array(range(trainset[-1] + 1, com_df.shape[0]))

# set Date as index
com_df.set_index('Date', inplace=True)

# find hedgeratio through linear regression least squares
model = sms.OLS(com_df.loc[:, 'Closing price_GLD'].iloc[trainset], com_df.loc[:, 'Closing price_GDX'].iloc[trainset])
result = model.fit()
hedgeratio = result.params
hedgeratio[0]

spread = com_df.loc[:,'Closing price_GLD'] - hedgeratio[0] * com_df.loc[:,'Closing price_GDX']



plt.figure(1)
plt.plot(spread.iloc[trainset])
plt.title('Spread trainset')
plt.figure(2)
plt.plot(spread.iloc[testset])
plt.title('Spread testset')

#calculate sprea
spreadMean = np.mean(spread.iloc[trainset])
spreadStd = np.std(spread.iloc[trainset])
zscore = (spread - spreadMean) / spreadStd

com_df['zscore'] = zscore

print("spreadMean: {0}".format(spreadMean))
print("spreadStd: {0}".format(spreadStd))

# Buy and Sell positions
com_df['GLD_positions'] = np.nan
com_df['GDX_positions'] = np.nan

com_df.loc[com_df['zscore']<=-2, ['GLD_positions', 'GDX_positions']] = [1, -1] #Buy long
com_df.loc[com_df['zscore']>=2, ['GLD_positions', 'GDX_positions']] = [-1, 1] #Buy short
com_df.loc[abs(com_df['zscore'])<=1, ['GLD_positions', 'GDX_positions']] = 0 #Exit position

# forward fill NaN values, excluding exit positions
com_df.fillna(method='ffill', inplace=True) #forward fill prices

positions = com_df.loc[:,('GLD_positions', 'GDX_positions')] # n x 2 matrix containing buy/sell positions. 
dailyret = com_df.loc[:, ['Closing price_GLD', 'Closing price_GDX']].pct_change() #calculates
PnL = (np.array(positions.shift()) * np.array(dailyret)).sum(axis=1) #shift one period because the first row in dailyret is NaN

SharpeTrainset = np.sqrt(252) * np.mean(PnL[trainset[1:]])/np.std(PnL[trainset[1:]])

print("SharpeTrainset: {0}".format(SharpeTrainset))

SharpeTestset = np.sqrt(252) * np.mean(PnL[testset])/np.std(PnL[testset])

print("SharpeTestset: {0}".format(SharpeTestset))

plt.figure(3)
plt.plot(np.cumsum(PnL[testset]))
plt.title('Cumulative profit & loss for testset')

plt.show()
#positions.to_pickle('example3_6_positions')
