import random
from copy import deepcopy

class Monkey():
    def __init__(self, window_size=50):
        self.possible_actions = ["buy","hold","sell"]
        self.window_size = window_size

    def init_random_weights(self):
        self.weights = [[random.random() for i in range(self.window_size+1)] for i in range(3)]
        return self

    def set_weights(self, weights):
        self.weights = weights

    def trade(self, df):
        """
            input: dataframe df of price of stock
            output: percentage gain

            give each monkey $1,000,000 to invest

        """

        capital = 1000000
        holdings = 0
        prices = df["price"].values

        def choose_action(params):
            """
                takes in params
                returns either buy, hold or sell
            """

            def dot(a,b):
                return sum([i*j for i,j in zip(a,b)])
            
            best_action, best_score = None, 0
            for action, weights in zip(["buy", "hold", "sell"], self.weights):
                score = dot(weights, params)

                if score > best_score:
                    best_score = score
                    best_action = action

            return best_action

        for i in range(self.window_size, len(prices)):
            price = prices[i]
            params = [holdings] + list(prices[i-self.window_size:i])
            action = choose_action(params)

            if holdings == 0 and action == "buy":
                # buy long
                n = int(capital/price)
                holdings += n
                capital -= n*price
            
            elif holdings == 0 and action == "sell":
                # sell short
                n = int(capital/price)
                holdings -= n
                capital += n*price

            elif holdings > 0 and action == "sell":
                # close long position
                capital += holdings*price
                holdings = 0

            elif holdings < 0 and action == "buy":
                # close short position
                capital += holdings*price
                holdings = 0

            else:
                action = "hold"

            if capital <= 0:
                return -100

        # closing all positions
        capital += holdings*price
        holdings = 0

        return (capital - 10**6) / 10**4



    # def trade_old(self, df, n=1):

    #     def choose_action(params):
    #         """
    #             takes in params
    #             returns either buy, hold or sell
    #         """

    #         def dot(a,b):
    #             return sum([i*j for i,j in zip(a,b)])
            
    #         best_action, best_score = None, 0
    #         for action, weights in zip(["buy", "hold", "sell"], self.weights):
    #             score = dot(weights, params)

    #             if score > best_score:
    #                 best_score = score
    #                 best_action = action

    #         return best_action

            

    #     profit = 0
    #     holdings = 0
    #     prices = df["price"].values

    #     for i in range(self.window_size, len(prices)):
    #         price = prices[i]
    #         action = choose_action([holdings] + list(prices[i-self.window_size:i]))

    #         if holdings == 0 and action == "buy":
    #             # buy long
    #             profit -= price * n
    #             holdings += n

    #         elif holdings == 0 and action == "sell":
    #             # sell short
    #             profit += price * n
    #             holdings -= n

    #         elif holdings > 0 and action == "sell":
    #             # close long position
    #             profit += price * holdings
    #             holdings = 0

    #         elif holdings < 0 and action == "buy":
    #             # close short position
    #             profit += price * holdings
    #             holdings = 0
            
    #         else:
    #             action = "hold"

    #     # closing all positions
    #     profit += price * holdings

    #     return profit

    def trade_pool(self, pool):
        """
            trades many stocks
            input:
                pool 
                    dictionary where
                        key = stock symbol
                        value = dataframe representing stock price

            output:
                dictionary where
                    key = stock
                    value = profit for stock
        """

        return {symbol:self.trade(df) for symbol,df in pool.items()}



    def breed(monkeys, epsilon=0.7, mutate_probability=0.3):
        """
            takes in an array of monkeys
            create 1 new monkey based on given array of monkeys
            returns this new monkey

            epsilon of the time:
                mutate one of the monkeys

            (1-epsilon) of the time:
                combine all of the monkeys
        """

        if random.random() < epsilon:
            parent = random.sample(monkeys,1)[0]
            weights = deepcopy(parent.weights)

            for line in weights:
                for i in range(len(line)):
                    if random.random() < mutate_probability:
                        line[i] += random.random() * 0.5 * random.sample([1,-1],1)[0]

            monkey = Monkey()
            monkey.set_weights(weights)

            return monkey

        else:
            parent_weights = [parent.weights for parent in monkeys]
            combined = []

            def combine(ls_of_ls):
                """
                    takes in list of lists, each with length x
                    returns 1 list with length x, combined with elements from all lists
                """
                out = []
                for i in range(len(ls_of_ls[0])):
                    out.append(ls_of_ls[random.randrange(len(ls_of_ls))][i])
                return out

            for i in range(3):
                row =  [parent_weights[j][i] for j in range(len(parent_weights))]
                combined.append(combine(row))

            monkey = Monkey()
            monkey.set_weights(combined)

            return monkey