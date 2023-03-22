from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np

class Trader:

    midpoints = []

    def run(self, state: TradingState) -> Dict[str, List[Order]]:

        result = {}

        for product in state.order_depths.keys():

            if product == 'PEARLS':
                
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []

                inventory_limit_long = 20
                inventory_limit_short = -20
                inventory_current = state.position.get('PEARLS', 0)
                max_buy = inventory_limit_long - inventory_current
                max_sell = inventory_limit_short - inventory_current

                if len(order_depth.sell_orders) and len(order_depth.buy_orders) != 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    midpoint = (best_ask + best_bid)/2

                Trader.midpoints.append(midpoint)  
                
                if len(Trader.midpoints) > 15:
            
                    std = 1.00 * np.std(Trader.midpoints[-15:])
                    threshold = np.mean(Trader.midpoints[-15:])

                    if best_ask < (threshold - 1.3/std):
                       orders.append(Order(product, best_ask, min(-best_ask_volume, max_buy)))

                    if best_bid > (threshold + 1.3/std): 
                        orders.append(Order(product, best_bid, max(-best_bid_volume, max_sell)))

                result[product] = orders

            if product == 'BANANAS':

                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []

                inventory_limit_long = 20
                inventory_limit_short = -20
                inventory_current = state.position.get('BANANAS', 0)
                max_buy = inventory_limit_long - inventory_current
                max_sell = inventory_limit_short - inventory_current

                if len(order_depth.sell_orders) and len(order_depth.buy_orders) != 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]

                if len(order_depth.sell_orders) != 0:
                     sp = list(order_depth.sell_orders.keys())
                     sv = list(order_depth.sell_orders.values())
                     offer_VWAP = sum([x*y for x,y in zip(sp, sv)])/sum(order_depth.sell_orders.values())

                if len(order_depth.buy_orders) != 0:
                     bp = list(order_depth.buy_orders.keys())
                     bv = list(order_depth.buy_orders.values())
                     bid_VWAP = sum([x*y for x,y in zip(bp, bv)])/sum(order_depth.buy_orders.values())

                if len(order_depth.sell_orders) and len(order_depth.buy_orders) != 0: 
                    acceptable_price = int((bid_VWAP+offer_VWAP)/2)

                if len(order_depth.sell_orders) != 0:
                    if best_ask <= acceptable_price:
                        orders.append(Order(product, best_ask, min(-best_ask_volume, max_buy)))

                if len(order_depth.buy_orders) != 0:
                    if best_bid >= acceptable_price:
                        orders.append(Order(product, best_bid, max(-best_bid_volume, max_sell)))
                
                result[product] = orders

        return result










