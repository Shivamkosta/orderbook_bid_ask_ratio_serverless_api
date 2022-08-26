# from utils import util
import sys
sys.path.append('../')
from utility.util import isValidDate

validCoins = ['BTC', 'ETH']
validTimeframes = ['1m', '5m', '15m', '1h', '4h', '1d']
validExchanges = ['Binance', 'Bitmex', 'Bitfinex', 'Bybit',
                  'Derbit', 'Ftx', 'Huobi', 'HuobiQtrly', 'Okex', 'OkexQtrly']
validLimits = [5, 10, 20, 50, 100, 500, 1000]
validOrderSizeBucket = ["1", "2", "3", "4", "5", "6", "7"]

def validate(reqParams):
    if(("coin" not in reqParams ) or ("tf" not in reqParams )):
        return {"isValid":False,"message":"Required params are missing."}
    if("coin" in reqParams and reqParams['coin'] not in validCoins):
        return {"isValid":False,"message":"Must be a valid coin."}
    if('tf' in reqParams and reqParams['tf'] not in validTimeframes):
        return {"isValid":False,"message":"Must be a valid timeFrame."}
    # if("exchange" in reqParams and reqParams['exchange'] and reqParams['exchange'] not in validExchanges):
    if("exchange" in reqParams and reqParams['exchange']):
        for x in reqParams['exchange']:
            if(x not in validExchanges):
                return {"isValid":False,"message":"Must be a valid exchange."}   
    if('startTime' in reqParams and isValidDate(reqParams['startTime'])):
        return {"isValid":False,"message":"must be a valid start time."}
    if('endTime' in reqParams and isValidDate(reqParams['endTime'])):
        return {"isValid":False,"message":"must be a valid end time."}
    if('startTime' in reqParams and 'endTime' in reqParams and not reqParams['startTime'] < reqParams['endTime']):
        return {"isValid":False,"message":"start time should be less than end time."}
    if('limit' in reqParams and reqParams['limit'] not in validLimits):
        return {"isValid":False,"message":"must be a valid limit."}
    # if('orderSizeBucket' in reqParams and reqParams['orderSizeBucket'] not in validOrderSizeBucket):
    if('orderSizeBucket' in reqParams and reqParams['orderSizeBucket']):
        for x in reqParams['orderSizeBucket']:
            if(x not in validOrderSizeBucket):
                return {"isValid":False, "message": "must be a valid orderSize"}    

    return {"isValid":True,"message":"Valid Params"}


