from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd


class stock_option:
    """
    This class retrieves and stores available options pricing data for
    a security can run one or more algorithms to identify optimal trades
    return this list of optimal trades
    """

    def __init__(self, security, buy_max, sell_min, demo_mode=False):
        """
        receives symbol of a security, maximum buy price, and minimum sale
        queries yahoo finance for options data, constructing a data frame of
        strike prices and current bids on sales of contracts for all available
        within 12 months.
        """
        self._security = security.upper()
        self._demo_mode = demo_mode
        self._timestamp = int(datetime.now().timestamp())
        self._buy_max = buy_max
        self._sell_min = sell_min
        self._pricing_data = pd.DataFrame()
        self._update_price_data()

    def get_stock_info(self):
        """
        returns ticker and value assignments of object
        """
        return [self._security, self._buy_max, self._sell_min]

    def _load_demo_price_data(self):
        """
        updates pricing data stored in object by loading files from ./data
        note, will throw error if matching file name is not found
        """
        self._pricing_data = \
            pd.read_csv("./data/" + self._security.lower() + ".csv")

    def _update_price_data(self):
        """
        updates options prices stored in object
        if demo mode is set, updates from files in ./data
        else, updates from web
        """
        if self._demo_mode is True:
            self._load_demo_price_data()
        else:
            self._update_price_data_from_web()

    def _update_price_data_from_web(self):
        """
        updates pricing data stored in object by querying yahoo finance
        """
        print("refreshing options data on " + self._security)
        column_names = ["name",
                        "posix_close_date",
                        "ticker",
                        "type",
                        "strike",
                        "bid",
                        "ask"]
        self._pricing_data = pd.DataFrame(columns=column_names)
        # get dates of available contracts
        data_url = ("https://finance.yahoo.com/quote/" +
                    self._security + "/options")
        pulled_data = requests.get(data_url)
        data_html = pulled_data.content
        content = BeautifulSoup(data_html, "html.parser")
        options_tables = content.find_all("table")
        dates = content.find_all("option")
        posix_dates = []
        dates_text = []
        for i in range(0, len(dates)):
            posix_dates.append(dates[i].get("value"))
            dates_text.append(dates[i].text)
        # create data frame for storage of pricing information
        for date in posix_dates:
            # shape formatted uri that incluudes contract date
            data_url = ("https://finance.yahoo.com/quote/" +
                        self._security + "/options?p=" +
                        self._security + "&date=" + date)
            # example URI
            # https://finance.yahoo.com/quote/PG/options?p=PG&date=1616716800
            pulled_data = requests.get(data_url)
            data_html = pulled_data.content
            content = BeautifulSoup(data_html, "html.parser")
            options_tables = content.find_all("table")
            for table in options_tables:
                rows = table.find_all("tr")[1:]
                cells = rows[0].find_all("td")
                if_put = cells[0].text.split(self._security)[1].find("P") > -1
                if_call = cells[0].text.split(self._security)[1].find("C") > -1
                if if_put:
                    contract_type = "put"
                elif if_call:
                    contract_type = "call"
                else:
                    contract_type = "error"
                    print("error assigning contract type")
                for row in rows:
                    cells = row.find_all("td")
                    if cells[4].text == "0.00" or \
                       cells[4].text == "-" or cells[5].text == "-":
                        pass
                    else:
                        strike_price = float(cells[2].text.replace(",", ""))
                        last_bid = float(cells[4].text.replace(",", ""))
                        if cells[5].text == "-":
                            last_ask = 0.0
                        else:
                            last_ask = float(cells[5].text.replace(",", ""))

                        self._pricing_data.loc[len(self._pricing_data)] \
                            = [str(cells[0].text),
                                date,
                                self._security,
                                contract_type,
                                strike_price,
                                last_bid,
                                last_ask]
        self._timestamp = int(datetime.now().timestamp())

    def update_value_prices(self, buy_max=None, sell_min=None):
        """
        changes the ticker valuation price points
        can adjust either or both the minimum and max
        if a price value is not passed, the original value is kept
        """
        if buy_max is not None:
            self._buy_max = buy_max
        if sell_min is not None:
            self._sell_min = sell_min

    def calculate_best(self, algorithm="naive_best_daily"):
        """
        receives name of algorithm
        calculates the best  options trade given the user's constraints
        return contract description for sale decision with highet income rate
        if data are 10 minutes old or errored, attempt to update data first
        if dataare incomplete, or algorithm returns empty set, return None
        note, currently passess parameters to naive_best for 20% depreciation
        and minimum contract proceeds of $20
        """
        selected = None
        if self._timestamp < int(datetime.now().timestamp()) - 600:
            self._update_price_data()
        if self._pricing_data.empty:
            selected = self._pricing_data
            print(self._security + " is empty")
        elif algorithm == "naive_best_daily":
            parameters = [.2, 0]
            selected = self._naive_best_daily(parameters)
        return(selected)

    def _naive_best_daily(self, parameters):
        """
        simple algorithm for demo purposes. identifies high return per day
        receives list containing annualized devaluation and minimum
        contract earnings acceptable to the user.
        Note this is currently hard coded to .20 and 0 respectively
        reports best valued put and call option, if available,
        given constraints and available contracts
        """
        annual_value_depreciation = parameters[0]
        minimum_contract_price = parameters[1]
        sufficient_earnings = self._pricing_data["bid"] > \
            minimum_contract_price
        df = self._pricing_data[sufficient_earnings]

        # calculate per day income from sale of option at current rate
        df["time_from_now"] = \
            df["posix_close_date"].astype("int") - self._timestamp

        # if contract date is less than a day, change these to 1 day
        df.loc[df.time_from_now < 86400, "time_from_now"] = 86400
        df["days_from_now"] = (df["time_from_now"] / 86400) + 1
        df["income_per_day"] = ((df["bid"] * 100) / df["days_from_now"])

        df["depreciated_strike"] = \
            df["strike"] - \
            (df["strike"] *
             ((df["days_from_now"]/365) *
                annual_value_depreciation))

        df["appreciated_strike"] = \
            df["strike"] + \
            (df["strike"] *
                ((df["days_from_now"]/365) *
                 annual_value_depreciation))

        df["income_per_dollar"] = df["income_per_day"] / (df["strike"] * 100)

        df = df.sort_values("income_per_day", ascending=False)
        meets_sell = df["depreciated_strike"] >= self._sell_min
        call = df["type"] == "call"
        selected_call = df[(meets_sell & call)].head(1)

        df = df.sort_values("income_per_dollar", ascending=False)
        meets_buy = df["appreciated_strike"] <= self._buy_max
        put = df["type"] == "put"
        selected_put = df[meets_buy & put].head(1)

        return pd.concat([selected_call, selected_put])
