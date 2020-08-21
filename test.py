import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.style.use("dark_background")

def plot(df, name):
    dfNp = np.array(df)
    mean = np.mean(dfNp)
    m = np.median(dfNp)
    std = np.std(dfNp)
    sweetSweetFrame = df.loc[df < 3000]

    print("STD", std)
    print("mean", mean)
    print("median", m)

    sweetSweetFrame.plot.hist(bins=100)
    """
    Insertion Time time only
    1   || Datafram length 644
    1 || Datafram length 970
    2 || STD 8816.13762502606
    3 || mean 1225.4209563503427
    4 || median 289.0841505001149

    1   || Datafram length 644
    1 || Datafram length 970
    2 || STD 8816.13762502606
    3 || mean 1225.4209563503427
    4 || median 289.08415050011496

    NO Insertion Time time only


    ThePrimeagen 1127
    || STD 4092.1784666863027
    || mean 735.4323119038451
    || median 261.72505501017

    Teeeeeeej 736
    || STD 1797.9185813307938
    || mean 555.4564003767608
    || median 282.116503
    """

    plt.title(name)
    plt.xlim([0, 3000])
    plt.show()

def getDataSet(path, isinList = False, invertList = False, insertionTimeOnly = True):

    df = pd.read_csv(path, dtype={"TotalTime": float})

    if isinList:
        inList = df["KeyStrokes"].isin(isinList)
        if invertList:
            df = df[~inList]
        else:
            df = df[inList]

    totalTime = df["TotalTime"] * 1000     #.plot.hist(bins=10, alpha=0.5)

    if insertionTimeOnly:
        for i in range(1, 4):
            totalTime -= df[f"Stroke{i}"] * 1000

    print("Datafram length", len(df))
    return totalTime


isinList = ["o", "O", "i", "I", "a", "A"]
invertList = False
insertionTimeOnly = True

tj = getDataSet("~/tj.apm.csv", isinList=isinList, invertList=invertList, insertionTimeOnly=insertionTimeOnly)
me = getDataSet("~/apm.csv", isinList=isinList, invertList=invertList, insertionTimeOnly=insertionTimeOnly)

frames = [tj, me]

plot(pd.concat(frames, sort=False), "All")

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
