from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np


class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:

        result = {}

        for product in state.order_depths.keys():

            # if product == 'BANANAS':
                
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                
                if len(order_depth.sell_orders) > 0:
                    sp = (list(order_depth.sell_orders.keys())) # offer prices
                    sv = (list(order_depth.sell_orders.values())) # offer volumes
                    offer_VWAP = sum([x*y for x,y in zip(sp, sv)])/sum(order_depth.sell_orders.values())
                    print(offer_VWAP)

                if len(order_depth.buy_orders) > 0:
                    bp = (list(order_depth.buy_orders.keys())) # bid prices
                    bv = (list(order_depth.buy_orders.values())) # bid volumes
                    bid_VWAP = sum([x*y for x,y in zip(bp, bv)])/sum(order_depth.buy_orders.values())
                    print(bid_VWAP)

                acceptable_price = (bid_VWAP+offer_VWAP)/2

                # BUY ORDER EXECUTION:
                if len(order_depth.sell_orders) > 0:
                    # for price in sp: 
                    for price, v_price in order_depth.sell_orders.items():
                        if price < acceptable_price:
                            # print("BUY",str(-order_depth.sell_orders[price]) + " " + str(product) + " AT", price)
                            orders.append(Order(product, price, -v_price))

                # SELL ORDER EXECUTION: 
                if len(order_depth.buy_orders) > 0:
                    # for price in bp: 
                    for price, v_price in order_depth.buy_orders.items():
                        if price > acceptable_price:
                            # print("SELL",str(order_depth.buy_orders[price]) + " " + product + " " + "AT", price)
                            orders.append(Order(product, price, -v_price))
                
                result[product] = orders
    
        return result