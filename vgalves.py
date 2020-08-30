import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# this package must be installed from the source using the command
# pip install git+https://github.com/tillahoffmann/asymmetric_kde.git
from asymmetric_kde import ImproperGammaEstimator

# pip install git+https://github.com/garrettj403/SciencePlots.git
plt.style.use(["science", "notebook", "vibrant", "high-vis"])
# if you do not like the beauty and pain of using latex
#  uncomment the line below and comment the plt.style lone above
# plt.style.use(["science", "no-latex", "notebook", "vibrant", "high-vis"])

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


def getDataSet(path, isinList=False, invertList=False, insertionTimeOnly=True):

    df = pd.read_csv(path)
    # clean non numeric on totalTime array and NAN
    df["TotalTime"] = pd.to_numeric(df["TotalTime"], errors="coerce")
    df = df.loc[~df["TotalTime"].isna()]

    if isinList:
        inList = df["KeyStrokes"].isin(isinList)
        if invertList:
            df = df[~inList]
        else:
            df = df[inList]

    totalTime = df["TotalTime"] * 1000  # .plot.hist(bins=10, alpha=0.5)

    if insertionTimeOnly:
        for i in range(1, 4):
            totalTime -= df[f"Stroke{i}"] * 1000

    print("Dataframe length", len(df))

    return totalTime


if __name__ == "__main__":

    isinList = ["o", "O", "i", "I", "a", "A"]
    isinList2 = ["cw", "cc", "ci*", "cf*", "ct*", "ca*", "C"]
    isinList3 = ["dwi", "di**", "df**", "dt**", "da**"]
    invertList = False
    insertionTimeOnly = False

    print("HERE IS MY FILE TJ")
    tj = getDataSet(
        "data/out.csv",
        isinList=isinList2,
        invertList=False,
        insertionTimeOnly=insertionTimeOnly,
    )
    tj.name = "Cs"

    print("HERE IS MY FILE Primeagen")
    me = getDataSet(
        "data/out.csv",
        isinList=isinList3,
        invertList=False,
        insertionTimeOnly=insertionTimeOnly,
    )
    me.name = "Ds"

    iandAs = getDataSet(
        "data/out.csv",
        isinList=isinList,
        invertList=False,
        insertionTimeOnly=insertionTimeOnly,
    )
    iandAs.name = "IAO"

    # concatenate both as columns
    frames = pd.concat([tj, me, iandAs], sort=False, axis=1)
    frames.boxplot(showfliers=False)
    plt.ylabel("InsertTime (ms)")
    plt.show()

    # Plot histograms

    for col in frames.columns:
        data = frames[col].dropna()
        plot(data, col)
        plt.xlabel("InsertTime (ms)")

    # plot asymmetrical density estimator
    # I does not assume gaussian distribution.
    fig, ax = plt.subplots()
    max_time = 3000
    time_array = np.linspace(0, max_time, 100000)
    for col in frames.columns:
        data = frames[col].dropna()
        sweetSweetFrame = data.loc[data < max_time]
        ige = ImproperGammaEstimator(sweetSweetFrame, "plugin")
        ax.plot(time_array, ige(time_array), label=col)
        ax.set_xlim([0, 1000])
        ax.set_xlabel("NeoVim - InsertTime (ms)")
        ax.set_ylabel("probability density function (PDF)")
        ax.set_title("kernel density estimation using asymmric kernels")
        plt.legend()
    plt.show()

