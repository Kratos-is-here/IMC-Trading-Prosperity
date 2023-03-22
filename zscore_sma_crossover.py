from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np
import statistics

# : (-1 * correlation(open, volume, 10)) -> 2.5
def corr(x,y,d):
    return statistics.correlation(x[-d:], y[-d:])
    # return np.std(np.dot(x[-d:],y[-d:]))/(np.std(x[-d:])*np.std(y[-d:]))

def zscore(x):
    stdd = np.std(x)
    if stdd == 0:
        return 0
    return (x - np.mean(x)) / stdd
def sma(x, d):
    return np.mean(x[-d:])

lim = {}
lim["BANANAS"] = 20
lim["PEARLS"] = 20
lim["COCONUTS"] = 600
lim["PINA_COLADAS"] = 300

# taking Z score of moving average for difference in prices lookback of 5 and 15,
# Buy when z score < -1
# Sell when z score > 1

class Trader:
    
    midpoints = {}
    # va = []
    # vb = []

    def run(self, state: TradingState) -> Dict[str, List[Order]]:

        result = {}
        
        # print(f"Current Position:{pos}")

        for product in state.order_depths.keys():
                order_depth: OrderDepth = state.order_depths[product]
                # Order Book Calcs
                if len(order_depth.sell_orders) and len(order_depth.buy_orders) != 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    midpoint = (best_ask + best_bid)/2
                if product in Trader.midpoints.keys():
                    Trader.midpoints[product].append(midpoint)
                else:
                    Trader.midpoints[product] = [midpoint]
        
        pos_pina = state.position.get('PINA_COLADAS', 0)
        pos_coco = state.position.get('COCONUTS', 0)
        diff_pina_coco = [a_i - b_i for a_i, b_i in zip(Trader.midpoints["PINA_COLADAS"], Trader.midpoints['COCONUTS'])]

        if min(len(Trader.midpoints['PINA_COLADAS']), len(Trader.midpoints['COCONUTS'])) >= 15:
            
            orders_p: list[Order] = []
            orders_c: list[Order] = []
            long_sma = sma(diff_pina_coco, 15)
            short_sma = sma(diff_pina_coco, 5)
            
            zs = zscore(long_sma-short_sma)
            
            # zs = (long_sma-short_sma)/np.std(long_sma)
            
            # switch the conditions
            
            if zs > 1/2: #and spread < 3:
                print("BUY", str(-best_ask_volume) + "x", best_ask)
                orders_p.append(Order('PINA_COLADAS', best_ask, min(lim['PINA_COLADAS']-pos_pina, -best_ask_volume)))
                orders_c.append(Order('COCONUTS', best_ask, min(lim['COCONUTS']-pos_coco, -best_ask_volume)))
                
            if zs < 1/2:
                print("SELL", str(best_bid_volume) + "x", best_bid)
                orders_p.append(Order('PINA_COLADAS', best_bid, max(-(lim['PINA_COLADAS']+pos_pina), -best_bid_volume)))
                orders_c.append(Order('COCONUTS', best_bid, max(-(lim['COCONUTS']+pos_coco), -best_bid_volume)))
                
            result['COCONUTS'] = orders_c
            result['PINA_COLADAS'] = orders_p

        return result
# 