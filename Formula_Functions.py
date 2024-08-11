# Last updated: 07/23/2024
# Code containing all formulas used to get values such as EMA, MFV, position size, etc.

# !Subject to change!
def get_EMA(Val_today: float, EMA_yesterday: float, smoothing: float, days: int):
    '''
    Calculate the Exponential Moving Average (EMA) for a given day
        Parameters:
            Val_today (float): The actual value (e.g., stock price, sales, etc.) for the current day.
        EMA_yesterday (float): The EMA value for the previous day.
            smoothing (float): The smoothing factor applied to the EMA calculation.
                   days (int): The number of days over which the EMA is calculated (e.g., 20-day EMA).
                   
        Returning:
            EMA_today (float): The EMA value for the current day. This is the value being calculated.
    '''
    return ((Val_today * (smoothing / smoothing + days)) + EMA_yesterday * (1 - (smoothing / 1  + days)))
    
    
get_EMA()
    
