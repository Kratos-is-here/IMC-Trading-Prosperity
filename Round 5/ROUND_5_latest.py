from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import numpy as np

class Trader:

    dip_mp = []
    dip_macd = []
    
    bag_mp = []
    
    uku_mp = []
    uku_macd = []

    pic_mp = []
    pic_macd = []

    dolphins = []
    diff = []

    def run(self, state: TradingState) -> Dict[str, List[Order]]:   
        
        result = {}

        # dip optimal
        dip_s = -50
        dip_l = -150
        
        # uku optimal
        uku_s = -30
        uku_l = -85

        # pic optimal
        pic_s = -50
        pic_l = -175

        for product in state.order_depths.keys():

            if product == 'DIP':
                
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                inventory_limit_long = 300
                inventory_limit_short = -300
                inventory_current = state.position.get('DIP', 0)
                # print(f"DIP: {inventory_current}")
                max_buy = inventory_limit_long - inventory_current
                max_sell = inventory_limit_short - inventory_current

                if len(order_depth.sell_orders) and len(order_depth.buy_orders) != 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    midpoint = (best_ask + best_bid)/2
                
                Trader.dip_mp.append(midpoint)

                if len(order_depth.sell_orders) and len(order_depth.buy_orders) != 0 and len(Trader.dip_mp) >= dip_l:
                    sma = np.mean(Trader.dip_mp[dip_s:])
                    lma = np.mean(Trader.dip_mp[dip_l:])
                    macd = sma - lma
                    Trader.dip_macd.append(macd)
                    
                    if Trader.dip_macd[-2] > 0 and Trader.dip_macd[-1] < 0: 
                        print("SELL", str(max(-best_bid_volume, max_sell)) + "x", best_bid) 
                        orders.append(Order(product, best_bid, max(-best_bid_volume, max_sell)))

                    if Trader.dip_macd[-2] < 0 and Trader.dip_macd[-1] > 0:
                        print("BUY", str(min(-best_ask_volume, max_buy)) + "x", best_ask)
                        orders.append(Order(product, best_ask, min(-best_ask_volume, max_buy)))
                    
                    result[product] = orders

            if product == 'BAGUETTE':
                
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                inventory_limit_long = 150
                inventory_limit_short = -150
                inventory_current = state.position.get('BAGUETTE', 0)
                max_buy = inventory_limit_long - inventory_current
                max_sell = inventory_limit_short - inventory_current
                # Order Book Calcs

                if len(order_depth.sell_orders) and len(order_depth.buy_orders) != 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    midpoint = (best_ask + best_bid)/2
                    spread = best_ask - best_bid

                Trader.bag_mp.append(midpoint)    

                if len(Trader.bag_mp) > 10:
            
                    std =  0.8 * np.std(Trader.bag_mp[-10:])
                    threshold = np.mean(Trader.bag_mp[-10:])
                                    
                    if midpoint < (threshold - std) and spread < 2:
                       print("BUY", str(-best_ask_volume) + "x", best_ask)
                       orders.append(Order(product, best_ask, min(-best_ask_volume, max_buy)))

                    if midpoint > (threshold + std) and spread < 2:
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, max(-best_bid_volume, max_sell)))

                result[product] = orders

            if product == 'UKULELE':
                
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                inventory_limit_long = 70
                inventory_limit_short = -70
                inventory_current = state.position.get('UKULELE', 0)
                print(f"UKULELE: {inventory_current}")
                max_buy = inventory_limit_long - inventory_current
                max_sell = inventory_limit_short - inventory_current

                if len(order_depth.sell_orders) and len(order_depth.buy_orders) != 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    midpoint = (best_ask + best_bid)/2
                
                Trader.uku_mp.append(midpoint)

                if len(order_depth.sell_orders) and len(order_depth.buy_orders) != 0 and len(Trader.uku_mp) >= uku_l:
                    sma = np.mean(Trader.uku_mp[uku_s:])
                    lma = np.mean(Trader.uku_mp[uku_l:])
                    macd = sma - lma
                    Trader.uku_macd.append(macd)
                    
                    if Trader.uku_macd[-2] > 0 and Trader.uku_macd[-1] < 0: 
                        print("SELL", str(max(-best_bid_volume, max_sell)) + "x", best_bid) 
                        orders.append(Order(product, best_bid, max(-best_bid_volume, max_sell)))

                    if Trader.uku_macd[-2] < 0 and Trader.uku_macd[-1] > 0:
                        print("BUY", str(min(-best_ask_volume, max_buy)) + "x", best_ask)
                        orders.append(Order(product, best_ask, min(-best_ask_volume, max_buy)))

                    result[product] = orders

            if product == 'PICNIC_BASKETS':
                
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []
                inventory_limit_long = 70
                inventory_limit_short = -70
                inventory_current = state.position.get('PICNIC_BASKETS', 0)
                # print(f"PICNIC_BASKETS: {inventory_current}")
                max_buy = inventory_limit_long - inventory_current
                max_sell = inventory_limit_short - inventory_current

                if len(order_depth.sell_orders) and len(order_depth.buy_orders) != 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    midpoint = (best_ask + best_bid)/2
                
                Trader.pic_mp.append(midpoint)

                if len(order_depth.sell_orders) and len(order_depth.buy_orders) != 0 and len(Trader.pic_mp) >= pic_l:
                    sma = np.mean(Trader.pic_mp[pic_s:])
                    lma = np.mean(Trader.pic_mp[pic_l:])
                    macd = sma - lma
                    Trader.pic_macd.append(macd)
                    
                    if Trader.pic_macd[-2] > 0 and Trader.pic_macd[-1] < 0: 
                        print("SELL", str(max(-best_bid_volume, max_sell)) + "x", best_bid) 
                        orders.append(Order(product, best_bid, max(-best_bid_volume, max_sell)))

                    if Trader.pic_macd[-2] < 0 and Trader.pic_macd[-1] > 0:
                        print("BUY", str(min(-best_ask_volume, max_buy)) + "x", best_ask)
                        orders.append(Order(product, best_ask, min(-best_ask_volume, max_buy)))

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

            if product == 'PEARLS':
                
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []

                inventory_limit_long = 20
                inventory_limit_short = -20
                inventory_current = state.position.get('PEARLS', 0)
                # print(f"PEARLS: {inventory_current}")
                max_buy = inventory_limit_long - inventory_current
                max_sell = inventory_limit_short - inventory_current
                
                price = 10000
                
                if len(order_depth.sell_orders) != 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    if best_ask < price:
                        print("BUY", str(min(-best_ask_volume, max_buy)) + "x", best_ask)
                        orders.append(Order(product, best_ask, min(-best_ask_volume, max_buy)))
                
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > price:
                        print("SELL", str(max(-best_bid_volume, max_sell)) + "x", best_bid) 
                        orders.append(Order(product, best_bid, max(-best_bid_volume, max_sell)))
                
                result[product] = orders

            if product == 'PINA_COLADAS':
                
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []

                inventory_limit_long = 300
                inventory_limit_short = -300
                inventory_current = state.position.get('PINA_COLADAS', 0)
                # print(f"PEARLS: {inventory_current}")
                max_buy = inventory_limit_long - inventory_current
                max_sell = inventory_limit_short - inventory_current
                
                price = 14900
                
                if len(order_depth.sell_orders) != 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    if best_ask < price:
                        print("BUY", str(min(-best_ask_volume, max_buy)) + "x", best_ask)
                        orders.append(Order(product, best_ask, min(-best_ask_volume, max_buy)))
                
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > price:
                        print("SELL", str(max(-best_bid_volume, max_sell)) + "x", best_bid) 
                        orders.append(Order(product, best_bid, max(-best_bid_volume, max_sell)))
                
                result[product] = orders


            if product == 'DIVING_GEAR':

                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []

                inventory_limit_long = 50
                inventory_limit_short = -50
                inventory_current = state.position.get('DIVING_GEAR', 0)
                # print(f"CO_P: {inventory_current}")
                # print(f"DS: {state.observations['DOLPHIN_SIGHTINGS']}")
                max_buy = inventory_limit_long - inventory_current
                max_sell = inventory_limit_short - inventory_current

                if len(order_depth.sell_orders) and len(order_depth.buy_orders) != 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    midpoint = (best_ask + best_bid)/2

                Trader.dolphins.append(state.observations['DOLPHIN_SIGHTINGS'])

                if inventory_current == 0 and len(Trader.dolphins) > 15:

                    if np.std(Trader.dolphins[-15:]) > 1.25 and (Trader.dolphins[-15] > Trader.dolphins[-1]):
                        print("SELL", str(max(-best_bid_volume, max_sell)) + "x", best_bid) 
                        orders.append(Order(product, best_bid, max(-best_bid_volume, max_sell)))

                    if np.std(Trader.dolphins[-15:]) > 1.25 and (Trader.dolphins[-15] < Trader.dolphins[-1]):
                        print("BUY", str(min(-best_ask_volume, max_buy)) + "x", best_ask)
                        orders.append(Order(product, best_ask, min(-best_ask_volume, max_buy)))
 
                if inventory_current > 0 and np.std(Trader.dolphins[-15:]) < 0.3:
                        print("SELL", str(inventory_current) + "x", best_bid) 
                        orders.append(Order(product, best_bid, inventory_current))

                if inventory_current < 0 and np.std(Trader.dolphins[-15:]) < 0.3:
                        print("BUY", str(inventory_current) + "x", best_ask)
                        orders.append(Order(product, best_ask, -inventory_current))

                result[product] = orders   
        
            if product == 'BERRIES':
                
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []

                inventory_limit_long = 250
                inventory_limit_short = -250
                inventory_current = state.position.get('BERRIES', 0)
                # print(f"BERRIES: {inventory_current}")
                max_buy = inventory_limit_long - inventory_current
                max_sell = inventory_limit_short - inventory_current

                if len(order_depth.sell_orders) and len(order_depth.buy_orders) != 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    spread = best_ask - best_bid
                    quote_offer = best_ask - 1
                    quote_bid = best_bid + 1

                # BUYING MM
                if spread >= 6:   
                        orders.append(Order(product, quote_bid, -best_ask_volume))
                        print(f"Buy {-best_ask_volume} {product} @ {quote_bid}")

                # SELLING MM
                if spread >=6:      
                        orders.append(Order(product, quote_offer, -best_bid_volume))
                        print(f"Sell {-best_bid_volume} {product} @ {quote_offer}")

                result[product] = orders   

            # if product == 'PICNIC_BASKET':
                
            #     order_depth: OrderDepth = state.order_depths[product]
            #     orders: list[Order] = []
            #     inventory_limit_long = 70
            #     inventory_limit_short = -70
            #     inventory_current = state.position.get('PICNIC_BASKET', 0)
            #     print(f"PICNIC_BASKET: {inventory_current}")
            #     max_buy = inventory_limit_long - inventory_current
            #     max_sell = inventory_limit_short - inventory_current

            #     if len(order_depth.sell_orders) and len(order_depth.buy_orders) != 0:
            #         best_ask = min(order_depth.sell_orders.keys())
            #         best_ask_volume = order_depth.sell_orders[best_ask]
            #         best_bid = max(order_depth.buy_orders.keys())
            #         best_bid_volume = order_depth.buy_orders[best_bid]
            #         midpoint = (best_ask + best_bid)/2

            #     Trader.pic_mp.append(midpoint)
  
            #     if len(Trader.dip_mp) > 2 and len(Trader.bag_mp) > 2 and len(Trader.uku_mp) > 2 and len(Trader.pic_mp) > 2:
            #         index = Trader.dip_mp[-1]*4 + Trader.bag_mp[-1]*2 + Trader.uku_mp[-1]
            #         diff = Trader.pic_mp[-1] - index
            #         Trader.diff.append(diff)

            #     if len(Trader.diff) > 10:

            #         if np.mean(Trader.diff[-10]) < Trader.diff[-1]:
            #             print("BUY", str(min(-best_ask_volume, max_buy)) + "x", best_ask)
            #             orders.append(Order(product, best_ask, min(-best_ask_volume, max_buy)))

            #         if np.mean(Trader.diff[-10]) > Trader.diff[-1]:
            #             print("SELL", str(max(-best_bid_volume, max_sell)) + "x", best_bid) 
            #             orders.append(Order(product, best_bid, max(-best_bid_volume, max_sell)))

        return result





            


    
            
                
                


