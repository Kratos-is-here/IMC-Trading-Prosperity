from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np

# : (-1 * correlation(open, volume, 10)) -> 2.5
def corr(x,y,d):
    # x_simple = np.array([-2, -1, 0, 1, 2])
    # y_simple = np.array([4, 1, 3, 2, 0])
    return np.std(np.dot(x[-d:],y[-d:]))/(np.std(x[-d:])*np.std(y[-d:]))
    
lim = {}
lim["COCONUTS"] = 600
lim["PINA_COLADAS"] = 300
class Trader:
    midpoints = []
    va = []
    vb = []

    def run(self, state: TradingState) -> Dict[str, List[Order]]:

        result = {}

        pos = state.position.get(product, 0)
        
        print(f"Current Position:{pos}")

        for product in state.order_depths.keys():

            # if product == 'COCONUTS':
                
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []

                # Order Book Calcs

                if len(order_depth.sell_orders) and len(order_depth.buy_orders) != 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    midpoint = (best_ask + best_bid)/2
                    spread = best_ask - best_bid
                    Trader.va.append(best_ask_volume)
                    Trader.vb.append(best_bid_volume)
                Trader.midpoints.append(midpoint)    

                if len(Trader.midpoints) > 1:
            
                    std = 1.00 * np.std(Trader.midpoints[-15:])
                    threshold = np.mean(Trader.midpoints[-15:])
                    
                    # z = (np.sign((best_ask_volume -Trader.va[-2])) * (-1 * (midpoint - Trader.midpoints[-2])))
                    # y = (np.sign((best_bid_volume -Trader.vb[-2])) * (-1 * (midpoint - Trader.midpoints[-2])))
                    
                    # (((sum(high, 20) / 20) < high) ? (-1 * delta(high, 2)) : 0) 
                    thresh = 0.5
                    z = -corr(Trader.midpoints, Trader.va, 15)
                    y = -corr(Trader.midpoints, Trader.vb, 15)

                    if z > thresh: #and spread < 3:/
                    # if best_ask < (threshold - .8): #and spread < 3:
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, min(lim[product]-pos, -best_ask_volume)))
                    if y < thresh:
                    # if best_bid > (threshold + .8): #and spread < 3:
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, max(-(lim[product]+pos), -best_bid_volume)))

                result[product] = orders

        return result
