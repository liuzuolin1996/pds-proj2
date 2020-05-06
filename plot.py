import matplotlib.pyplot as plt
import pickle

data = pickle.load(open("saved/AAPL.sav", "rb"))

avg = [i["average"] for i in data]
high = [i["high"] for i in data]
low = [i["low"] for i in data]

plt.plot(avg, color="red")
plt.plot(high, color="green")
plt.plot(low, color="blue")

plt.show()
