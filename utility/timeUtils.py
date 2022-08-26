from datetime import datetime


def _range(start_time, end_time, steps, type = "datetime"):
    range = []
    start_time = (start_time - (start_time % steps)) - steps
    end_time = (end_time - (end_time % steps))
    tempTimeFrame = start_time
    while tempTimeFrame < end_time:
        tempTimeFrame = tempTimeFrame + steps
        if type == "number":
            range.append(tempTimeFrame*1000)
        else:
            range.append(datetime.utcfromtimestamp(tempTimeFrame))
        # range.append(tempTimeFrame)
    return range

def getTimeFrameGap(timeframe):
    if timeframe == '1m':
        return 60
    elif timeframe == '5m':
        return 300
    elif timeframe == '15m':
        return 900
    elif timeframe == '1h':
        return 3600
    elif timeframe == '4h':
        return 14400
    elif timeframe == '1d':
        return 86400
    else:
        return 60
