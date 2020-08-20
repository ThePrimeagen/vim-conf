import matplotlib.pyplot as plt
import pandas as pd

plt.style.use("dark_background")
df = pd.read_csv('~/apm.csv', dtype={"TotalTime": float})

totalTime = df["TotalTime"] * 1000     #.plot.hist(bins=10, alpha=0.5)
totalTime = totalTime.drop(50)

print(totalTime.head)
totalTime.plot.hist(bins=[0, 100, 200, 500, 1000, 2000, 5000, 1000000], logx=True)
plt.show()

# df["TARGET"] = df.TitalTime.apply(lambda x: "short" if x<0.3 else ("medium" if x<=0.6 else "long"))

"""
grouped = df.groupby("KeyBucket")
for name, group in grouped:
    total = group["TotalTime"] * 1000     #.plot.hist(bins=10, alpha=0.5)
    total.plot.hist(bins=[0, 100, 200, 500, 1000, 2000, 5000, 1000000], logx=True)
    plt.title(name)
    plt.show()

"""
"""
grouped = df.groupby("KeyBucket")
print(grouped.groups)

for name, group in grouped:
    print(name)
    group.plot(kind='scatter', x='KeyStrokes', y='TotalTime',color='red')
    plt.show()

"""
"""
xAxis = []
yAxis = []

file = open("", "r")

for x in range(0, 3):
    xAxis.append(x)
    yAxis.append(x / 3)

plt.style.use("dark_background")
plt.scatter(xAxis, yAxis)
plt.title('title name')
plt.xlabel('xAxis name')
plt.ylabel('yAxis name')
plt.show()
"""
