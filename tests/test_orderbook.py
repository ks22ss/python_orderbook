import unittest
from orderbook_management.orderbook import *
from collections import deque

class TestOrderBook(unittest.TestCase):

    def test_limit_order_placing_1(self):
        orderbook = Orderbook()
        orderbook.place_limit_order(LimitOrderInfo("A01",20, 100,'bid'))
        with self.assertRaises(Exception) as context:
            orderbook.place_limit_order(LimitOrderInfo("A01",19, 100,'ask'))
            self.assertTrue('[Error] limit price exceed current bid.' in context.exception)

    def test_limit_order_placing_2(self):
        orderbook = Orderbook()
        orderbook.place_limit_order(LimitOrderInfo("A01",20, 100,'bid'))
        orderbook.place_limit_order(LimitOrderInfo("A01",22, 200,'ask'))
        with self.assertRaises(Exception) as context:
            orderbook.place_limit_order(LimitOrderInfo("A01",24, 300,'bid'))
            self.assertTrue('[Error] limit price exceed current ask.' in context.exception)

    def test_market_order_placing_3(self):
        orderbook = Orderbook()
        orderbook.place_limit_order(LimitOrderInfo("LO00001",25, 100,'bid'))
        orderbook.place_limit_order(LimitOrderInfo("LO00002",25, 200,'bid'))
        orderbook.place_limit_order(LimitOrderInfo("LO00003",24, 300,'bid'))
        orderbook.place_limit_order(LimitOrderInfo("LO00004",23, 250,'bid'))
        
        orderbook.place_market_order(MarketOrderInfo("MO00001",50,'bid'))
        self.assertEqual(orderbook.book, {
                25: deque([{'id': 'LO00002', 'volume': 150, 'side': 'bid'}, 
                            {'id': 'LO00001', 'volume': 100, 'side': 'bid'}]), 
                24: deque([{'id': 'LO00003', 'volume': 300, 'side': 'bid'}]),
                23: deque([{'id': 'LO00004', 'volume': 250, 'side': 'bid'}])
            })

    
    def test_market_order_placing_4(self):
        orderbook = Orderbook()
        orderbook.place_limit_order(LimitOrderInfo("LO00001",25, 100,'ask'))
        orderbook.place_limit_order(LimitOrderInfo("LO00002",25, 200,'ask'))
        orderbook.place_limit_order(LimitOrderInfo("LO00003",24, 300,'ask'))
        orderbook.place_limit_order(LimitOrderInfo("LO00004",23, 250,'ask'))
        
        orderbook.place_market_order(MarketOrderInfo("MO00001",50,'ask'))
        self.assertEqual(orderbook.book, {
            25: deque([{'id': 'LO00002', 'volume': 200, 'side': 'ask'}, 
                        {'id': 'LO00001', 'volume': 100, 'side': 'ask'}]), 
            24: deque([{'id': 'LO00003', 'volume': 300, 'side': 'ask'}]), 
            23: deque([{'id': 'LO00004', 'volume': 200, 'side': 'ask'}])
        })

    def test_market_order_placing_5(self):
        orderbook = Orderbook()
        orderbook.place_limit_order(LimitOrderInfo("LO00001",25, 100,'ask'))
        orderbook.place_limit_order(LimitOrderInfo("LO00002",25, 150,'ask'))
        orderbook.place_limit_order(LimitOrderInfo("LO00003",24, 50,'ask'))
        orderbook.place_limit_order(LimitOrderInfo("LO00004",23, 200,'ask'))
        
        orderbook.place_market_order(MarketOrderInfo("MO00001",500,'ask'))
        self.assertEqual(orderbook.book, {})


    def test_market_order_placing_6(self):
        orderbook = Orderbook()
        orderbook.place_limit_order(LimitOrderInfo("LO00001",25, 100,'bid'))
        orderbook.place_limit_order(LimitOrderInfo("LO00002",25, 150,'bid'))
        orderbook.place_limit_order(LimitOrderInfo("LO00003",24, 50,'bid'))
        orderbook.place_limit_order(LimitOrderInfo("LO00004",23, 200,'bid'))
        
        orderbook.place_market_order(MarketOrderInfo("MO00001",500,'bid'))
        self.assertEqual(orderbook.book, {})


    def test_market_order_placing_7(self):
        orderbook = Orderbook()
        orderbook.place_limit_order(LimitOrderInfo("LO00001",27, 100,'ask'))
        orderbook.place_limit_order(LimitOrderInfo("LO00002",25, 150,'ask'))
        orderbook.place_limit_order(LimitOrderInfo("LO00003",24, 50,'ask'))
        orderbook.place_limit_order(LimitOrderInfo("LO00004",23, 200,'ask'))
        
        orderbook.place_market_order(MarketOrderInfo("MO00001",450,'ask'))
        self.assertEqual(orderbook.book, {27: deque([{'id': 'LO00001', 'volume': 50, 'side': 'ask'}])})

    def test_market_order_placing_8(self):
        orderbook = Orderbook()
        orderbook.place_limit_order(LimitOrderInfo("LO00002",13, 150,'ask'))
        orderbook.place_limit_order(LimitOrderInfo("LO00003",12, 50,'bid'))
        with self.assertRaises(Exception) as context:
            orderbook.place_market_order(MarketOrderInfo("MO00001",0,'bid'))
            self.assertTrue("[Error] order.volume must be larger than 0." in context.exception)

    def test_market_order_placing_9(self):
        orderbook = Orderbook()
        orderbook.place_limit_order(LimitOrderInfo("LO00002",13, 150,'ask'))
        orderbook.place_limit_order(LimitOrderInfo("LO00003",12, 50,'bid'))
        with self.assertRaises(Exception) as context:
            orderbook.place_market_order(MarketOrderInfo("MO00001",0,'mark'))
            self.assertTrue("[Error] order.side is either 'bid' and 'ask'." in context.exception)


if __name__ == '__main__':
    unittest.main()