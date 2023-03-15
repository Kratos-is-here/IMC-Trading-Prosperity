"""
Data Model Example: 
"""

import json
from typing import Dict, List
import numpy as np
from json import JSONEncoder
# from banana_march_15_v2 import Trader
# from datamodel import *

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
    def __init__(self, buy_orders: dict, sell_orders: dict):
        self.buy_orders: Dict[int, int] = buy_orders
        self.sell_orders: Dict[int, int] = sell_orders
# class OrderDepth:
#     def __init__(self, buy_orders: dict, sell_orders: dict):
#         self.buy_orders: buy_orders
#         self.sell_orders: sell_orders
    # def __len__(self)

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
d1 = {10: 7, 9: 5}
d2 = {11: -4, 10: -8}
timestamp = 1000
odpt_b = OrderDepth(buy_orders=d1, sell_orders=d2)
odpt_s = OrderDepth(buy_orders=d1, sell_orders=d2)
# print(odpt_b.buy_orders)
listings = {"BANANAS": Listing(symbol="BANANAS",product="BANANAS", denomination="BANANAS"),"SHELLS": Listing(symbol="SHELLS", product="SHELLS", denomination="SHELLS")}

order_depths = {"BANANAS": odpt_b,"SHELLS": odpt_s}

own_trades = {"BANANAS": [],"SHELLS": []}

market_trades = {"BANANAS": [Trade(symbol="BANANAS",price=11,quantity=4,buyer="",seller="",)],"SHELLS": []}

position = {"BANANAS": 0,"SHELLS": 0}

observations = {}

state = TradingState(timestamp=timestamp,listings=listings,order_depths=order_depths,own_trades=own_trades,market_trades=market_trades,position=position,observations=observations)

########################################################################################

"""
Algorithm
"""

# class Trader:

#     def run(self, state: TradingState) -> Dict[str, List[Order]]:

#         result = {}
       
#         for product in state.order_depths.keys():
             
#             if product == 'SHELLS': 

#                 order_depth: OrderDepth = state.order_depths[product]
#                 orders: list[Order] = []
                
#                 acceptable_price = 11
                
#                 # Buy Orders
#                 if len(order_depth.sell_orders) > 0:
#                     best_ask = min(order_depth.sell_orders.keys())
#                     best_ask_volume = order_depth.sell_orders[best_ask]
#                     if best_ask < acceptable_price:
#                         print("BUY", str(-best_ask_volume) + "x", best_ask)
#                         orders.append(Order(product, best_ask, -best_ask_volume))
               
#                # Sell Orders
#                 if len(order_depth.buy_orders) != 0:
#                     best_bid = max(order_depth.buy_orders.keys())
#                     best_bid_volume = order_depth.buy_orders[best_bid]
#                     if best_bid > acceptable_price:
#                         print("SELL", str(best_bid_volume) + "x", best_bid)
#                         orders.append(Order(product, best_bid, -best_bid_volume))

#                 result[product] = orders
    
#         return result

# class Trader:

#     def run(self, state: TradingState) -> Dict[str, List[Order]]:

#         result = {}
    
#         for product in state.order_depths.keys():

#             # if product == "BANANAS":
                
#                 order_depth: OrderDepth = state.order_depths[product]
#                 orders: list[Order] = []
#                 bid_VWAP = 0
#                 offer_VWAP = 0
#                 # print(order_depth)
#                 # print(order_depth.sell_orders)
                
#                 if len(order_depth.sell_orders) > 0:
#                     sp = np.array(list(order_depth.sell_orders.keys())) # offer prices
#                     sv = np.array(list(order_depth.sell_orders.values())) # offer volumes
#                     offer_VWAP = sum([x*y for x,y in zip(sp, sv)])/sum(order_depth.sell_orders.values())
#                     print(offer_VWAP)

#                 if len(order_depth.buy_orders) > 0:
#                     bp = np.array(list(order_depth.buy_orders.keys())) # offer prices
#                     bv = np.array(list(order_depth.buy_orders.values())) # offer volumes
#                     bid_VWAP = sum([x*y for x,y in zip(bp, bv)])/sum(order_depth.buy_orders.values())
#                     print(bid_VWAP)

#                 acceptable_price = (bid_VWAP+offer_VWAP)/2
#                 if len(order_depth.sell_orders) != 0:
#                     best_ask = min(order_depth.sell_orders.keys())
#                     best_ask_volume = order_depth.sell_orders[best_ask]
#                     if best_ask < acceptable_price:
#                         print("BUY", str(-best_ask_volume) + "x", best_ask)
#                         orders.append(Order(product, best_ask, -best_ask_volume))
                
#                 if len(order_depth.buy_orders) != 0:
#                     best_bid = max(order_depth.buy_orders.keys())
#                     best_bid_volume = order_depth.buy_orders[best_bid]
#                     if best_bid > acceptable_price:
#                         print("SELL", str(best_bid_volume) + "x", best_bid)
#                         orders.append(Order(product, best_bid, -best_bid_volume))
                
#                 result[product] = orders
    
#         return result


class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:

        result = {}

        for product in state.order_depths.keys():

            # if product == 'BANANAS':
                
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                
                if len(order_depth.sell_orders) != 0:
                    sp = np.array(list(order_depth.sell_orders.keys())) # offer prices
                    sv = np.array(list(order_depth.sell_orders.values())) # offer volumes
                    offer_VWAP = sum([x*y for x,y in zip(sp, sv)])/sum(order_depth.sell_orders.values())
                    # print(offer_VWAP)

                if len(order_depth.buy_orders) != 0:
                    bp = np.array(list(order_depth.buy_orders.keys())) # bid prices
                    bv = np.array(list(order_depth.buy_orders.values())) # bid volumes
                    bid_VWAP = sum([x*y for x,y in zip(bp, bv)])/sum(order_depth.buy_orders.values())
                    print(bid_VWAP)

                acceptable_price = (bid_VWAP+offer_VWAP)/2 # 13 

                # BUY ORDER EXECUTION:
                for price in sp: 
                    if price < acceptable_price:
                        print("BUY",str(-order_depth.sell_orders[price]) + " " + product + " AT", price)
                        orders.append(Order(product, price, -order_depth.sell_orders[price]))

                # SELL ORDER EXECUTION: 
                for price in bp: 
                    if price > acceptable_price:
                        print("SELL",str(order_depth.buy_orders[price]) + " " + product + " AT", price)
                        orders.append(Order(product, price, order_depth.buy_orders[price]))
                
                result[product] = orders
    
        return result

########################################################################################
x = Trader()
print("Hi")
print(state.order_depths['BANANAS'])
print(x.run(state))
print("Hi2")

# write a prograam for mean reversion strategy for the given Order book