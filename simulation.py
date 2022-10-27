import sys 
sys.path.append("../")
from orderbook_management.orderbook import *
import numpy as np
import uuid
import time
import datetime

orderbook = Orderbook()
LOT_SIZE = 100
SIGMA = 15
warmup = 20
i = 0
while True:
    print("\n\n")
    print(f"Current Time: {datetime.datetime.now().strftime('%Y-%m-%d %HH%MM%SS')}")

    id = str(uuid.uuid4())
    volume = np.random.randint(1,10)*LOT_SIZE
    side = np.random.choice(a=['bid','ask'])
    if i > warmup:
        types = np.random.choice(a=['market','limit'])
    else:
        types = 'limit'
    try:
        
        if types == 'market':
            if side == 'bid':
                orderbook.place_market_order(MarketOrderInfo(id, volume, side), log=True)
            elif side == 'ask':
                orderbook.place_market_order(MarketOrderInfo(id, volume, side), log=True)

        elif types == 'limit':
            if side == 'bid':
                lowest_ask = orderbook.lowest_ask()
                if lowest_ask == None:
                    price = np.random.randint(1,100)
                    orderbook.place_limit_order(LimitOrderInfo(id, price, volume, side), log=True)
                else:
                    price = np.floor(np.random.normal(lowest_ask, SIGMA, 1)[0])
                    while price > lowest_ask or price < 1:
                        price = np.floor(np.random.normal(lowest_ask, SIGMA, 1)[0])

                    orderbook.place_limit_order(LimitOrderInfo(id, price, volume, side), log=True)

            elif side == 'ask':
                highest_bid = orderbook.highest_bid()
                if highest_bid == None:
                    price = np.random.randint(1,100)
                    orderbook.place_limit_order(LimitOrderInfo(id, price, volume, side), log=True)
                else:
                    price = np.ceil(np.random.normal(highest_bid, SIGMA, 1)[0])
                    while price < highest_bid or price > 100:
                        price = np.ceil(np.random.normal(highest_bid, SIGMA, 1)[0])

                    orderbook.place_limit_order(LimitOrderInfo(id, price, volume, side), log=True)
    except:
        pass
    
    orderbook.show()
    
    if i > warmup:
        time.sleep(3)

    i+=1