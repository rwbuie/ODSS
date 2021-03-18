from stock_option import stock_option as so
import pandas as pd
from datetime import datetime


class portfolio:
    """
    This class reads a given portfolio file and creates a series of stock
    objects in order to identify the best options trades to make in current
    market conditions.
    receives file and strategy name
    """

    def __init__(self, file, demo_mode=False, strategy="naive_best_daily"):
        """
        receives portfolio file name, demo setting, and strategy option
        loads a file containing stock positions and trade preferences
        stores ticker and data on each ticker
        prints trade recommendations for the portfolio
        """
        self._file = file
        self._strategy = strategy
        self._demo_mode = demo_mode
        self._portfolio = []
        self._cash_position = 0
        self._read_portfolio()
        self.print_portfolio()
        self._timestamp = int(datetime.now().timestamp())
        self._optimum_trades = pd.DataFrame()
        self._optimize_strategy()

    def print_portfolio(self):
        """
        prints current portfolio and cash position to screen
        """
        print()
        print("portfolio:")
        for stock, holding in self._portfolio:
            ticker, buy, sell = stock.get_stock_info()
            print(str(holding) + " shares of " + str(ticker) +
                  " with max buy price of " + str(buy) +
                  " and min sale price of " + str(sell))
        print()
        print("cash = " + str(self._cash_position))

    def change_demo_mode(self, demo_mode=False):
        """
        receives desired demo setting
        changes demo mode setting if necessary
        reloads data if mode is changed
        """
        if demo_mode != self._demo_mode:
            self._demo_mode = demo_mode
            print("Demo status changed to " + print(demo_mode) + ".")
            print("Reloading data")
            self._read_portfolio
        else:
            print("Demo status unchanged.")

    def _read_portfolio(self):
        """
        called by consturctor, reads object's portfolio file
        and loads data into object
        """
        df = pd.read_csv(self._file)
        for i, data in df.iterrows():
            if data["ticker"] == "cashposition":
                self._cash_position = data["shares"]
            else:
                self._portfolio.append([so(data["ticker"],
                                        data["buy"],
                                        data["sell"],
                                        self._demo_mode),
                                        data["shares"]])

    def current_strategy(self):
        """
        returns the current strategy to the user
        """
        return(self._strategy)

    def report_trades(self):
        """
        called by user to view current investment recommendations
        returns object's optomized trades
        """
        return(self._optimum_trades)

    def _optimize_strategy(self):
        """
        updates portfolio recommendations given current strategy setting
        """
        if self._strategy == "naive_best_daily":
            column_names = ["name",
                            "ticker",
                            "type",
                            "strike",
                            "bid",
                            "ask",
                            "income_per_day",
                            "count"]
            self._optimum_trades = pd.DataFrame(columns=column_names)
            kept_puts = pd.DataFrame(columns=column_names)
            for column in self._portfolio:
                stock = column[0]
                df = stock.calculate_best(self._strategy)
                df["count"] = 0
                if df.shape[0] > 0:
                    call = df["type"] == "call"
                    put = df["type"] == "put"
                    df.loc[call, ["count"]] = column[1] // 100
                    self._optimum_trades = \
                        pd.concat([self._optimum_trades, df[call]
                                  [column_names]])
                    kept_puts = pd.concat([kept_puts, df[put]])
            if kept_puts.shape[0] > 0:
                kept_puts["most_contracts_in"] = self._cash_position // \
                                                (kept_puts["strike"] * 100)
                kept_puts["actual_earnable"] = \
                    kept_puts["income_per_dollar"] * \
                    kept_puts["most_contracts_in"]
                kept_puts = kept_puts.sort_values("actual_earnable",
                                                  ascending=False)
                cash_tally = self._cash_position
                selected_puts = []
                for i in kept_puts.index:
                    kept_puts.loc[i, ["count"]] = cash_tally // \
                        int(kept_puts.loc[i, ["strike"]] * 100)
                    if ((kept_puts.loc[i, ["count"]].empty is False) and
                       (kept_puts.loc[i, ["count"]] // 1 > 0).bool()):
                        cash_tally = cash_tally - \
                                    (kept_puts.loc[i, ["count"]] *
                                     (kept_puts.loc[i, ["strike"]] * 100))

                        selected_puts.append(i)
                kept_puts = kept_puts.loc[selected_puts][column_names]

            self._optimum_trades = pd.concat([self._optimum_trades, kept_puts])
            self._optimum_trades["income_per_day"] = (
                self._optimum_trades["income_per_day"] *
                self._optimum_trades["count"])
