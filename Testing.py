"""
Data Model Example: 
"""

import json
from typing import Dict, List
from json import JSONEncoder

Time = int
Symbol = str
Product = str
Position = int
UserId = str
Observation = int

class Listing:
    def __init__(self, symbol: Symbol, product: Product, denomination: Product):
        self.symbol = symbol
        self.product = product
        self.denomination = denomination

class Order:
    def __init__(self, symbol: Symbol, price: int, quantity: int) -> None:
        self.symbol = symbol
        self.price = price
        self.quantity = quantity

    def __str__(self) -> str:
        return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"

    def __repr__(self) -> str:
        return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"
    
class OrderDepth:
    def __init__(self, buy_orders: dict, sell_orders = dict):
        self.buy_orders: Dict[int, int] = {}
        self.sell_orders: Dict[int, int] = {}

class Trade:
    def __init__(self, symbol: Symbol, price: int, quantity: int, buyer: UserId = "", seller: UserId = "") -> None:
        self.symbol = symbol
        self.price: int = price
        self.quantity: int = quantity
        self.buyer = buyer
        self.seller = seller

    def __str__(self) -> str:
        return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ")"

    def __repr__(self) -> str:
        return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ")"

class TradingState(object):
    def __init__(self,
                timestamp: Time,
                listings: Dict[Symbol, Listing],
                order_depths: Dict[Symbol, OrderDepth],
                own_trades: Dict[Symbol, List[Trade]],
                market_trades: Dict[Symbol, List[Trade]],
                position: Dict[Product, Position],
                observations: Dict[Product, Observation]):
        self.timestamp = timestamp
        self.listings = listings
        self.order_depths = order_depths
        self.own_trades = own_trades
        self.market_trades = market_trades
        self.position = position
        self.observations = observations
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)   

class ProsperityEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

########################################################################################
"""
State Example: 
"""

timestamp = 1000

listings = {"PRODUCT1": Listing(symbol="PRODUCT1",product="PRODUCT1", denomination="PRODUCT1"),"PRODUCT2": Listing(symbol="PRODUCT2", product="PRODUCT2", denomination="PRODUCT2")}

order_depths = {"PRODUCT1": OrderDepth(buy_orders={10: 7, 9: 5},sell_orders={11: -4, 12: -8}),"PRODUCT2": OrderDepth(buy_orders={142: 3, 141: 5},sell_orders={144: -5, 145: -8})}

own_trades = {"PRODUCT1": [],"PRODUCT2": []}

market_trades = {"PRODUCT1": [Trade(symbol="PRODUCT1",price=11,quantity=4,buyer="",seller="",)],"PRODUCT2": []}

position = {"PRODUCT1": 0,"PRODUCT2": 0}

observations = {}

state = TradingState(timestamp=timestamp,listings=listings,order_depths=order_depths,own_trades=own_trades,market_trades=market_trades,position=position,observations=observations)

########################################################################################

"""
Algorithm
"""

class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:

        result = {}

        for product in state.order_depths.keys():

            if product == 'PRODUCT2': 

                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                
                acceptable_price = 11
                
                # Buy Orders
                if len(order_depth.sell_orders) > 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    if best_ask < acceptable_price:
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_volume))
                
                # Sell Orders
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > acceptable_price:
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))

                result[product] = orders
    
        return result

########################################################################################

Trader.run(Trader,state)