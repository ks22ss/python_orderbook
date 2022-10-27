from orderbook_management.orderbook import *

if __name__ == '__main__':
    orderbook = Orderbook()
    orderbook.place_limit_order(LimitOrderInfo("LO00001",25, 100,'ask'))
    orderbook.place_limit_order(LimitOrderInfo("LO00002",25, 150,'ask'))
    orderbook.place_limit_order(LimitOrderInfo("LO00003",24, 50,'ask'))
    orderbook.place_limit_order(LimitOrderInfo("LO00004",23, 200,'ask'))
    orderbook.place_limit_order(LimitOrderInfo("LO00001",12, 100,'bid'))
    orderbook.place_limit_order(LimitOrderInfo("LO00002",21, 150,'bid'))
    orderbook.place_limit_order(LimitOrderInfo("LO00003",21, 50,'bid'))
    orderbook.place_limit_order(LimitOrderInfo("LO00004",19, 200,'bid'))

    print(orderbook.lowest_ask())
    print(orderbook.highest_bid())

    print(orderbook.show())

 