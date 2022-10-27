from ast import Or
from collections import deque
from dataclasses import dataclass
from shutil import ExecError

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
        for price_level, order_list in self.book.items():
            new_book[price_level] = list(filter(lambda order_info: order_info['side'] == side, order_list))
        return self.remove_empty_order_lists(new_book)

    def sort_book_by_price(self, book, side):
        reverse = False
        if side == 'bid':
            reverse = True
        return sorted(book.items(), reverse=reverse)

    # Order Placing
    def place_limit_order(self, order: LimitOrderInfo):
        if order.price not in self.book:
            self.add_new_price(order.price)

        self.validate_side_input(order)
        self.validate_price_input(order)

        self.book[order.price].appendleft({'id':order.id, 'volume':order.volume, 'side':order.side})
    
    def place_market_order(self, order: MarketOrderInfo):
        self.validate_side_input(order)
        self.validate_volume_input(order)

        new_book = self.filter_book_by_side(order.side)
        new_book = self.sort_book_by_price(new_book, order.side)

        current_vol = order.volume
        i = 0
        while current_vol > 0:
            
            price_level = new_book[i][0]
            order_lists = new_book[i][1]

            for order_info in order_lists:
                #print(order_info)
                if current_vol >= order_info['volume']:
                    self.book[price_level].popleft()
                    current_vol -= order_info['volume']
                else:
                    self.book[price_level][0]['volume'] -= current_vol
                    current_vol = 0
            i += 1

        self.book = self.remove_empty_order_lists(self.book)
        


if __name__ == '__main__':
    orderbook = Orderbook()
    orderbook.place_limit_order(LimitOrderInfo("A01",20, 100,'bid'))
    orderbook.place_limit_order(LimitOrderInfo("A01",20, 100,'ask'))
    orderbook.place_limit_order(LimitOrderInfo("A01",20, 100,'bid'))
    print(orderbook.book)
