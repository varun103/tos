from trade_log_processor import Trade
from trade_log_processor import TradesProcessor
import csv
from dateutil import parser
import pprint
from util import Color

FILE = '/Users/varunajmera/Documents/accnt-stmt.csv'
COMM = 0.65
FIND = 'AMD'


class Account_Stmt_Processor:

    def __init__(self):
        self._ledger = {}
        self._state = {}

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

            stock = row[4]

            if FIND and FIND != stock:
                continue

            time = row[0]
            if len(time) > 1:
                date = parser.parse(time)

            # print(row)
            comm = COMM
            q = row[3]
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

            if stock not in self._state.keys():
                self._state[stock] = 0
            self._state[stock] = self._state[stock] + int(q)

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

        print(Color.BOLD, key, '-', len(_tp.trades), Color.ENDC, _tp)

        pprint.pprint(_tp.stock)
        print('\n')

    secured = 0
    _sec = []
    for p in tp.stock.keys():
        if a._state[p] == 0:
            print(Color.HEADER, p, ':', tp.stock[p], Color.ENDC)
            secured = secured + tp.stock[p]
        else:
            print(Color.FAIL, p, ':', tp.stock[p], Color.ENDC)

    sec = sorted(_sec, key=lambda x: x[1], reverse=True)

    print(secured)
