from genetic_helper.classes.Monkey import Monkey
import pickle

class Genetic():
    def __init__(self, num_monkeys=100, monkey_window_size=20, num_keep=5, num_iter=100):
        self.num_monkeys = num_monkeys
        self.monkeys = [Monkey(window_size=monkey_window_size).init_random_weights() for i in range(num_monkeys)]
        self.num_keep = num_keep
        self.num_iter = num_iter

    def run(self, stock):
        """
            let monkeys trade the input stock
        """

        out = []

        for i in range(self.num_iter):
            strongest, stats = self.select_strongest(stock)
            self.monkeys = self.breed_monkeys(strongest)
            print(f"iteration {i+1}: stats: {stats} ")
            out.append(stats)
        
        return out

    def select_strongest(self, stock):
        scores = []
        for i,monkey in enumerate(self.monkeys):
            profit = monkey.trade(stock)
            scores.append((i, profit))
        
        scores.sort(key=lambda x:-x[1])

        avg = sum([j for i,j in scores])/len(scores)
        high = scores[0][1]
        low = scores[-1][1]

        return [self.monkeys[i] for i,j in scores[:self.num_keep]], {"average": avg, "high":high, "low":low}

    def breed_monkeys(self, strongest):
        """
            takes in x strongest monkets, and mutates them to create more children
        """

        out = []
        for i in range(self.num_monkeys - len(strongest)):
            monkey = Monkey.breed(strongest)
            out.append(monkey)
        
        return strongest + out

    def run_pool(self, pool):
        """
            let monkeys trade input list of stocks
        """
        out = []

        with open("stats.csv","w") as f:
            for i in range(self.num_iter):
                strongest, stats = self.select_strongest_using_pool(pool)
                self.monkeys = self.breed_monkeys(strongest)
                print(f"iteration {i+1}: stats: {stats} ")
                out.append(stats)

                pickle.dump(self.monkeys, open("saved/monkeys.sav", "wb"))
                f.write(str(stats["high"]) + "," + str(stats["average"]) + "," + str(stats["low"]) + "\n")

    
    def select_strongest_using_pool(self, pool):
        """
            get all n monkeys to trade on this pool of stocks
            select strongest monkeys based on overall average
        """

        scores = []

        for i,monkey in enumerate(self.monkeys):
            d = {}
            for stocksymbol, df in pool.items():
                gain = monkey.trade(df)
                d[stocksymbol] = gain
            
            d["aggregate"] = sum(d.values())/len(d)

            scores.append(d)

        scores = [(i,val) for i,val in enumerate(scores)]
        scores.sort(key=lambda x:-x[1]["aggregate"])

        strongest = [i for i,val in scores[:self.num_keep]]
        strongest = [self.monkeys[i] for i in strongest]

        scores = [val["aggregate"] for i,val in scores]
        
        return strongest, {"high": max(scores), "average": sum(scores)/len(scores), "low": min(scores)}
