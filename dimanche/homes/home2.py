import random
import os
import multiprocessing

class Home(multiprocessing.Process):
    def __init__(self, id, production_rate, consumption_rate, trade_policy):
        super().__init__()
        self.id = id
        self.production_rate = production_rate
        self.consumption_rate = consumption_rate
        self.trade_policy = trade_policy
        self.surplus = 0
        self.shortage = 0

    def update_surplus_shortage(self):
        self.surplus = self.production_rate - self.consumption_rate
        self.shortage = self.consumption_rate - self.production_rate

    def trade_energy(self, market_price):
        if self.trade_policy == 'always_give':
            return self.surplus
        elif self.trade_policy == 'always_sell':
            return -self.shortage
        else:  # self.trade_policy == 'sell_if_no_takers':
            if self.surplus > 0:
                return self.surplus
            elif self.shortage > 0 and market_price < threshold:
                return -self.shortage
            else:
                return 0

def generate_homes(num_homes):
    homes = []
    for i in range(num_homes):
        production_rate = random.uniform(0, 10)
        consumption_rate = random.uniform(0, 10)
        trade_policy = random.choice(['always_give', 'always_sell', 'sell_if_no_takers'])
        h=Home(i, production_rate, consumption_rate, trade_policy)
        h.start()
        homes.append(h)

    return homes

market_price = 0.15
threshold = 0.2
homes = generate_homes(10)
for home in homes:
    home.update_surplus_shortage()
    market_price += home.trade_energy(market_price)
    print("Home {} has surplus: {} and shortage: {}      {}".format(home.id, home.surplus, home.shortage, home.pid))
print("Market price is: {}".format(market_price))
