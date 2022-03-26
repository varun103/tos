from trade_log_processor import Trade
import csv

FILE='/Users/varunajmera/Documents/accnt-stmt.csv'
COMM = 0.65

class Account_Stmt_Processor:

    def __init__(self):
        self._ledger={}


    def process(self, file):
        f=open(file)
        c = csv.reader(f)
        for row in c:
            if row[1] == 'STOCK':
                continue
            print(row)
            comm = COMM
            q = row[3]
            stock=row[4]
            print(stock)
            amt = row[7]
            if stock == 'SPX':
                comm = 1.3
            comm = abs(float(q) * comm)
            cost = float(amt) * float(q) * 100 * -1
            print(comm)
            print(cost)
            total = cost + comm


class TradeA(Trade):

    def __init__(self, date, stock, total, comm):
        super().__init__(stock, total, comm)
        self.date = date



if __name__ == '__main__':

    a = Account_Stmt_Processor()
    a.process(FILE)