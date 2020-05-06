import pandas as pd
import random

class Parser():
    """
        preprocesses CSV files for time series data
    """
    
    def __init__(self, main_path="data/prices-split-adjusted.csv"):
        data = pd.read_csv(main_path)
        data["price"] = [(high+low)/2 for high,low in zip(data["high"], data["low"])]
        self.data = data

    def info(self):
        """
            shows overview of each stock
        """
        return self.data.loc[:,["symbol","open"]].groupby("symbol").count()
    
    def getAll(self, limit=1500):
        """
            gets all stocks which have >=limit rows
            
            returns dictionary where
                key = stock symbol
                value = pd.DataFrame containing price info
        """
        
        counts = self.data.loc[:, ["symbol","open"]].groupby("symbol", as_index=False).count()
        counts = {k:v for k,v in counts.values if v >= limit}
        
        return {k: self.get(v) for k,v in counts.items()}
            
    def get(self, symbol):
        """
            returns only the prices where symbol is input
            price in this case = (high + low) / 2 for simplicity
        """
        out = self.data[self.data["symbol"]==symbol]
        out = out.set_index("date")
        return out.loc[:,["price"]]

    def get_pool(self, n=10):
        """ 
            returns a dictionary
                key = stock symbol
                value = stock prices

            of n random stocks
        """

        symbols = set(self.data["symbol"].values)
        chosen = random.sample(symbols, n)

        print(f"chosen: {chosen}")

        return {k:self.get(k) for k in chosen}


if __name__ == "__main__":
    parser = Parser()
    apple = parser.get("AAPL")
    print(apple)
