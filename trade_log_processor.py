import os
from functools import reduce
import pprint

DIR = '/Users/varunajmera/Documents/mar'
FIND = ''


class Trade:

    def __init__(self, stock:str, total:int, comm:int):
        self.stock = stock
        self.total = total
        self.comm = comm
        self.net = total - comm

    def __str__(self):
        text = '{stock}, {total}, {commission}, {net}'
        return text.format(stock=self.stock, total=self.total, commission=self.comm, net=self.net)

    def __repr__(self):
        text = '{stock} :{total}, {commission}, {net}'
        return text.format(stock=self.stock, total=self.total, commission=self.comm, net=self.net)


class TradeProcessor:

    def __init__(self):
        self.options_legs = {
            'VERTICAL': 2,
            'SINGLE': 1,
            'BUTTERFLY': 4,
            'DIAGONAL': 2
        }
        self.type = {
            'SELL': 1,
            'BUY': -1
        }

    def process(self, stock, filename):

        file = open(filename)
        lines = file.readlines()
        total = 0
        commission_total = 0

        for line in lines:

            tokens = line.split(' ')

            type = tokens[0]
            multiplier = self.type[type] * 100

            lot_size = abs(int(tokens[1]))

            option_leg = tokens[2]
            if option_leg in self.options_legs.keys():
                trade_count = self.options_legs[option_leg]
            else:
                trade_count = 1

            commission = trade_count * .65 * lot_size

            price = tokens[-3].split('@')
            total = total + (float(price[1]) * multiplier * lot_size)
            commission_total = commission_total + commission

        total = int(total)
        commission_total = int(commission_total)

        t = Trade(stock, total, commission_total)
        return t


class TradesProcessor:


    def __init__(self, trades):
        self.trades = trades
        self.sorted_trades = sorted(trades, key=lambda trade:trade.net, reverse=True)
        self.total = 0
        self.comm = 0
        self.net = 0
        self.stock = {}
        self._process()

    def _process(self):

        trades = self.trades
        self.total = reduce(lambda a, b: a + b.total, trades, 0)
        self.comm = reduce(lambda a, b: a + b.comm, trades, 0)
        self.net = reduce(lambda a, b: a + b.net, trades, 0)
        for t in trades:
            if t.stock not in self.stock.keys():
                self.stock[t.stock] = 0
            self.stock[t.stock] = self.stock[t.stock] + t.net


    def __str__(self):
        x = "\nTotal = {trades}" \
            "\nCommission = {comm}" \
            "\nNet with commission = {net}" \
            "\nCommission %age = {c_p:.2f}\n"

        return x.format(trades= self.total, comm = self.comm, net = self.net, c_p = (self.comm / self.total) * 100)

if __name__ == '__main__':

    files = os.listdir(DIR)
    t = TradeProcessor()

    trades = []
    for filename in files:
        if filename.startswith('simulated'):
            _stock = filename.split('_')[2]
            stock = _stock.split('-')[0]
            dir_filename = DIR + '/' + filename
            if FIND:
                if FIND == stock:
                    trade = t.process(stock, dir_filename)
            else:
                trade = t.process(stock, dir_filename)

            trades.append(trade)


    t = TradesProcessor(trades)

    sorted_trades = sorted(trades, key=lambda trade:trade.net, reverse=True)
    for i in sorted_trades:
        print(i)

    print(t)

    pprint.pprint(t.stock)


