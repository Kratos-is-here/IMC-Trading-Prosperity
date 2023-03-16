from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np


def ema(lkback_period, data):
    emaval = 0
    days = 0
    smoothing = 2
    for x in data[-lkback_period::-1]:
        emaval = emaval * (1-smoothing/(1+days)) + x * (smoothing / (1 + days))
    return emaval

class Trader:    
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}
        for product in state.order_depths.keys():
            # if product == 'BANANAS':
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                
                smoothing = 1.5
                if len(order_depth.sell_orders) > 0:
                    sp = (list(order_depth.sell_orders.keys())) # offer prices
                    # sv = (list(order_depth.sell_orders.values())) # offer volumes

                    # days = 0
                    sell_long_ema = ema(50,sp)
                    sell_short_ema = ema(35,sp)
                    # for x in sp[::-1]:
                    #     sell_ema = sell_ema * (1-smoothing/(1+days)) + x * (smoothing / (1 + days))
                    #     days += 1
                    # sv = (list(order_depth.sell_orders.values())) # offer volumes
                    # offer_VWAP = sum([x*y for x,y in zip(sp, sv)])/sum(order_depth.sell_orders.values())
                    # print(offer_VWAP)

                if len(order_depth.buy_orders) > 0:
                    bp = (list(order_depth.buy_orders.keys())) # bid prices
                    # bv = (list(order_depth.buy_orders.values())) # bid volumes
                    # bid_VWAP = sum([x*y for x,y in zip(bp, bv)])/sum(order_depth.buy_orders.values())
                    # print(bid_VWAP)

                    # days = 0
                    
                    buy_long_ema = ema(50,bp)
                    buy_short_ema = ema(35,bp)
                        

                short_acceptable_price = (buy_short_ema + sell_short_ema) / 2
                long_acceptable_price = (buy_long_ema + sell_long_ema) / 2
                # acceptable_price = (bid_VWAP + offer_VWAP) / 2
                # acceptable_price = (acceptable_price + acceptable_price1) / 2
                
                # BUY ORDER EXECUTION:
                if len(order_depth.sell_orders) > 0:
                    # for price in sp: 
                    for price, v_price in order_depth.sell_orders.items():
                        # if price < buy_ema:
                        if price < short_acceptable_price:
                            # print("BUY",str(-order_depth.sell_orders[price]) + " " + str(product) + " AT", price)
                            orders.append(Order(product, price, -v_price))

                # SELL ORDER EXECUTION: 
                if len(order_depth.buy_orders) > 0:
                    # for price in bp: 
                    for price, v_price in order_depth.buy_orders.items():
                        if price > short_acceptable_price:
                        # if price > sell_ema:
                            # print("SELL",str(order_depth.buy_orders[price]) + " " + product + " " + "AT", price)
                            orders.append(Order(product, price, -v_price))
                
                result[product] = orders
    
        return result
