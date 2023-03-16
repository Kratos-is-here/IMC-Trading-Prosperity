from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np


class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:

        result = {}
    
        for product in state.order_depths.keys():

            # if product == "BANANAS":
                
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                bid_VWAP = 0
                offer_VWAP = 0
                print(order_depth)
                print(order_depth.sell_orders)
                
                if len(order_depth.sell_orders) > 0:
                    sp = np.array(list(order_depth.sell_orders.keys())) # offer prices
                    sv = np.array(list(order_depth.sell_orders.values())) # offer volumes
                    offer_VWAP = sum([x*y for x,y in zip(sp, sv)])/sum(order_depth.sell_orders.values())
                    print(offer_VWAP)

                if len(order_depth.buy_orders) > 0:
                    bp = np.array(list(order_depth.buy_orders.keys())) # offer prices
                    bv = np.array(list(order_depth.buy_orders.values())) # offer volumes
                    bid_VWAP = sum([x*y for x,y in zip(bp, bv)])/sum(order_depth.buy_orders.values())
                    print(bid_VWAP)

                acceptable_price = (bid_VWAP+offer_VWAP)/2
                if len(order_depth.sell_orders) > 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    if best_ask < acceptable_price:
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_volume))
                
                if len(order_depth.buy_orders) > 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > acceptable_price:
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))
                
                result[product] = orders
    
        return result
