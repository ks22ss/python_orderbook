from collections import deque
from dataclasses import dataclass
import numpy as np

@dataclass
class LimitOrderInfo:
    id: str
    price: float
    volume: int
    side: str

@dataclass
class MarketOrderInfo:
    id: str
    volume: int
    side: str

class Orderbook:
    def __init__(self) -> None:
        self.book = {}
    
    # Validations
    def validate_side_input(self, order):
        if order.side != "bid" and order.side != "ask":
            raise Exception("[Error] order.side is either 'bid' and 'ask'.")  

    def validate_volume_input(self, order):
        if order.volume <= 0:
            raise Exception("[Error] order.volume must be larger than 0.")  

    def validate_price_input(self, order):
        if order.side == 'bid':
            if len(self.filter_book_by_side('ask')) > 0 and order.price >= min(self.filter_book_by_side('ask').keys()):
                raise Exception("[Error] limit price exceed current ask.") 
        elif order.side == 'ask': 
            if len(self.filter_book_by_side('bid')) > 0 and order.price <= max(self.filter_book_by_side('bid').keys()):
                raise Exception("[Error] limit price exceed current bid.") 

    # Helper Functions
    def add_new_price(self, price):
        self.book[price] = deque([])
    
    def remove_empty_order_lists(self, book):
        return {k:v for k,v in book.items() if len(v) > 0}

    def filter_book_by_side(self, side):
        new_book = {}
        if len(self.book) == 0:
            return new_book
        for price_level, order_list in self.book.items():
            new_book[price_level] = list(filter(lambda order_info: order_info['side'] == side, order_list))
        return self.remove_empty_order_lists(new_book)

    def sort_book_by_price(self, book, side):
        reverse = False
        if side == 'bid':
            reverse = True
        return sorted(book.items(), reverse=reverse)


    def lowest_ask(self):
        ask_book = self.filter_book_by_side('ask')
        if len(ask_book) > 0:
            return min(ask_book.keys())



    def highest_bid(self):
        bid_book = self.filter_book_by_side('bid')
        if len(bid_book) > 0:
            return max(bid_book.keys())


    # Order Placing
    def place_limit_order(self, order: LimitOrderInfo , log=False):
        if order.price not in self.book:
            self.add_new_price(order.price)

        self.validate_side_input(order)
        self.validate_price_input(order)

        # FIFO
        self.book[order.price].appendleft({'id':order.id, 'volume':order.volume, 'side':order.side})
        if log:
            print(f"Limit order placed. [Pirce = {order.price}] [Volume = {order.volume}] [Side = {order.side}]")

    def place_market_order(self, order: MarketOrderInfo, log=False):
        self.validate_side_input(order)
        self.validate_volume_input(order)

        new_book = self.filter_book_by_side(order.side)
        new_book = self.sort_book_by_price(new_book, order.side)

        current_vol = order.volume
        i = 0
        exec_value = []
        while current_vol > 0:
            
            price_level = new_book[i][0]
            order_lists = new_book[i][1]

            for order_info in order_lists:
                #print(order_info)
                if current_vol >= order_info['volume']:
                    exec_value.append(order_info['volume'] * price_level)
                    self.book[price_level].popleft()
                    current_vol -= order_info['volume']
                else:
                    exec_value.append(current_vol * price_level)
                    self.book[price_level][0]['volume'] -= current_vol
                    current_vol = 0
            i += 1

        self.book = self.remove_empty_order_lists(self.book)
        if log:
            print(f"Market order placed. [Avg. Pirce = {round(sum(exec_value)/order.volume,2)}] [Volume = {order.volume}] [Side = {order.side}]")

    def show(self):
        print("--------------------------------")
        
        ask_orderbook = self.filter_book_by_side("ask")

        if len(ask_orderbook) > 0:
            ask_ladder = {price:sum([order['volume'] for order in order_lists]) for price,order_lists in ask_orderbook.items()}
            
            print("Ask")
            print(np.array(list(sorted(ask_ladder.items(), reverse=True))))

        bid_orderbook = self.filter_book_by_side("bid")

        if len(bid_orderbook) > 0:
            bid_ladder = {price:sum([order['volume'] for order in order_lists]) for price,order_lists in bid_orderbook.items()}
            print("Bid")
            print(np.array(list(sorted(bid_ladder.items(), reverse=True))))

        print("--------------------------------")

