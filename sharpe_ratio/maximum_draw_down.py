import numpy as np
import pandas as pd

def calc_cumulative_return(DailyReturns:np.array) -> np.array:
    cumret = np.array(DailyReturns)

    for i in range(1,len(cumret)):
        cumret[i] = (1 + cumret[i]) * (1 + cumret[i-1]) - 1 
    
    return cumret

def calculateMaxDD(ReturnArray:np.array) -> (float, int):
    """
        Returns tuple (maxmimum drawdown, maximum drawdown period)

        Input parameter:

            Cumret: a series consiting of the cumulative profit and loss curve.

        Output parameter:
            MaxDD:float - the maximum drawdown
            MaxPeriodDD:int - the duration of the longest drawdown period.     

    """   
    #initalisation
    highwatermark = np.zeros(len(ReturnArray)) 
    drawdown = np.zeros(len(ReturnArray))
    drawdownperiod = np.zeros(len(ReturnArray))

    for t in range(1, len(ReturnArray)):
        # highwater mark for time t, is the global maximum at any given time
        highwatermark[t] = max(highwatermark[t-1], ReturnArray[t])
        # calculate the ratio from global maximum to current point on cumlative return curve
        drawdown[t] = (1+highwatermark[t]) / (1+ReturnArray[t]) - 1
        # Calculate whether the drawdown period is still active or ended.
        if drawdown[t] == 0: # if current point on the curve is also the global maximum
            drawdownperiod[t] = 0
        else:
            drawdownperiod[t] = drawdownperiod[t-1] + 1 # increment the drawdown duration

    return max(drawdown), max(drawdownperiod)        
