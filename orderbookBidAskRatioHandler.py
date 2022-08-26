import sys
sys.path.append('../')
from utility.db import client
from email import message
import json
from multiprocessing import Process,  Pipe
from array import array
from utility.timeUtils import _range, getTimeFrameGap
from reqValidator import validExchanges
from reqValidator import validate
from utility.apiResponse import apiError, apiSuccess
from datetime import datetime
from operator import index


def getOrderBookBidAskRatio(event, context):
    obj = {}
    depthList = ['0', 'quote', '1', '2', '5', '10', '20','full']
    if ('coin' in event['queryStringParameters']):
        coin = event['queryStringParameters']['coin']
        obj['coin'] = coin
    if ('startTime' in event['queryStringParameters']):
        startTime = event['queryStringParameters']['startTime']
        obj['startTime'] = startTime
    if ('endTime' in event['queryStringParameters']):
        endTime = event['queryStringParameters']['endTime']
        obj['endTime'] = endTime
    if ('timeframe' in event['queryStringParameters']):
        timeframe = event['queryStringParameters']['timeframe']
        obj['tf'] = timeframe
    if ('exchange' in event['queryStringParameters']):
        exchange = event['queryStringParameters']['exchange'].split(',')
        obj['exchange'] = exchange
    else:
        obj['exchange'] = validExchanges
    if ('limit' in event['queryStringParameters']):
        limit = event['queryStringParameters']['limit']
        obj['limit'] = limit
    if ('depth' in event['queryStringParameters']):
        depth = event['queryStringParameters']['depth'].split(',')
        # depth = ['quote',1]
        obj['depth'] = depth
        ind1 = depthList.index(depth[0])
        ind2 = depthList.index(depth[1])
        print("================>>>>>>>>",ind1,ind2)
        if ind1 <= ind2:
            tempDepthList = []
            for i in range(ind1, ind2):
                tempDepthList.append(depthList[i])
            obj['depth'] = tempDepthList
            print("find depth=========>>>>>>>>",obj['depth'])
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Invalid depth limit specified"
                })
            }
    else:
        print("kuch to krna pdega!")
    if ('marketTypes' in event['queryStringParameters']):
        marketTypes = event['queryStringParameters']['marketTypes']
        obj['marketTypes'] = marketTypes

    start_time = obj['startTime']
    end_time = obj['endTime']
    time_range = _range(start_time, end_time,getTimeFrameGap(obj['tf']), 'number')
    validatorRes = validate(obj)
    myDb = client['ORDERBOOK_'+obj['coin']]
    print(myDb)
    processList = []
    parent_connections = []

    def function():
        if (not validatorRes["isValid"]):
            return apiError(400, "Bad Request")

        global checkingMp

        def checkingMp(exc, child_con):
            filterField = {}
            filterField['timestamp'] = 1
            filterField['_id'] = 0
            mapField = {
                'quote': 'quoteLevel',
                '1': 'depth1',
                '2': 'depth2',
                '5': 'depth5',
                '10': 'depth10',
                '20': 'depth20',
                'full': 'fullbook'
            }
            for bucket in obj['depth']:
                filterField["{0}.bidAskRatio".format(mapField[bucket])] = 1
            data = list(myDb[exc.lower()+"_"+obj['coin'].lower()].find(
                {'timestamp': {'$in': time_range}},
                filterField
            ))
            i = 0
            j = 0
            finalRes = {}
            if ('depth' not in event['queryStringParameters']):
                finalRes = {"depth": []}
            while i < len(time_range):
                if time_range[i] == data[j]['timestamp']:
                    if ('depth' in event['queryStringParameters']):
                        for depthSize in obj['depth']:
                            if depthSize not in finalRes:
                                finalRes[depthSize] = []
                            finalRes[depthSize].append(
                                [data[j][mapField[depthSize]]['bidAskRatio']])
                    i = i+1
                    j = j+1
                else:
                    finalRes[depthSize].append('null')

            child_con.send({"data": finalRes, "exchange": exc})

        if __name__ == "__main__":
            arr = obj['exchange']
            for a in arr:
                parent_conn, child_conn = Pipe()
                parent_connections.append(parent_conn)
                p = Process(target=checkingMp, args=(a, child_conn))
                processList.append(p)
    finalResult = {}

    finalResult['t'] = [x for x in time_range]
    function()
    for pr in processList:
        pr.start()
    for pr in processList:
        pr.join()
    pr_con = len(parent_connections)
    for parent_connection in parent_connections:
        orderBookBidAskDataTemp = parent_connection.recv()
        pr_con = pr_con - 1
        finalResult[orderBookBidAskDataTemp["exchange"]] = orderBookBidAskDataTemp["data"]
        if (pr_con == 0):
            print("finalResult=======================>>>>>>>>>", finalResult)
            return {'statusCode': 200, "body": json.dumps(finalResult)}


getOrderBookBidAskRatio({"queryStringParameters": {
    "coin": "BTC",
    "timeframe": '1m',
    "exchange": "Binance",
    "startTime": 1660808820,
    "endTime": 1660809000,
    "depth": "quote,full",
}}, "ty")
