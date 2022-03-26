from trade_log_processor import Trade
from trade_log_processor import TradesProcessor
import csv
import datetime
from dateutil import parser
import pprint

FILE = '/Users/varunajmera/Documents/accnt-stmt.csv'
COMM = 0.65


class Account_Stmt_Processor:

    def __init__(self):
        self._ledger = {}

    def process(self, file):
        f = open(file)
        c = csv.reader(f)
        trades = []
        date = None
        for row in c:
            if len(row) < 2:
                continue
            if row[1] == 'STOCK':
                continue

            time = row[0]
            if len(time) > 1:
                date = parser.parse(time)

            # print(row)
            comm = COMM
            q = row[3]
            stock = row[4]
            amt = row[7]
            if stock == 'SPX':
                comm = 1.3
            comm = abs(float(q) * comm)
            cost = float(amt) * float(q) * 100 * -1

            index = str(date.month) + '_' + str(date.year)


            t = TradeA(date, stock, cost, comm)
            trades.append(t)

            if index not in self._ledger.keys():
                self._ledger[index] = []
            self._ledger[index].append(t)

        return trades


class TradeA(Trade):

    def __init__(self, date, stock, total, comm):
        super().__init__(stock, total, comm)
        self.date = date


if __name__ == '__main__':
    a = Account_Stmt_Processor()
    ts = a.process(FILE)

    tp = TradesProcessor(ts)
    print(tp)

    pprint.pprint(tp.stock)

    for key in sorted(a._ledger.keys()):
        _tp = TradesProcessor(a._ledger[key])

        print(key, _tp,)
        pprint.pprint(_tp.stock)
        print('\n')
