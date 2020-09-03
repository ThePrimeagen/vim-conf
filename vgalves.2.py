import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re

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

    df = pd.read_csv(path, engine="c")
    # clean non numeric on totalTime array and NAN
    df["TotalTime"] = pd.to_numeric(df["TotalTime"], errors="coerce")
    df = df.loc[~df["TotalTime"].isna()]
    # df['KeyStrokes'].unique()
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


def get_dataset_regex_licenced(csv_path, list_of_cmd, insertionTimeOnly=True):
    """
        Load a dataset and filter based on the starting char of a vim command
    :param csv_path: path_to_csv_file
    :param list_of_cmd: string with the chars to capture,e.g. inserting mode chars 'aoi'
    :return:
    """

    # let it try to load and fail
    raw_df = pd.read_csv(csv_path)
    # clean non numeric on totalTime array and NAN
    raw_df["TotalTime"] = pd.to_numeric(raw_df["TotalTime"], errors="coerce")
    raw_df = raw_df.loc[~raw_df["TotalTime"].isna()]

    filtered_index = raw_df["KeyStrokes"].str.match(
        rf"^([{list_of_cmd}])", flags=re.IGNORECASE
    )

    filtered_df = raw_df.loc[filtered_index]
    total_time = filtered_df["TotalTime"] * 1000

    if insertionTimeOnly:
        for i in range(1, 4):
            total_time -= raw_df[f"Stroke{i}"] * 1000

    return total_time


if __name__ == "__main__":
    # comparing insert time between users
    users = {
        "TJ": "data/tj.apm.csv",
    }
    """
    users = {
        "ThePrimeagen": [
            ["data/apm.no-cdw.csv", "i", "d", "c"],
            ["data/apm.cdw.csv", "c", "d"]
        ],
        "TJ": [
            ["data/tj.apm.no-cdw.csv", "i", "d", "c"],
            ["data/tj.apm.cdw.csv", "c", "d"]
        ],
    }
    """

    keyBuckets = ["i", "a", "o", "d", "c"]

    insertionTimeOnly = False
    max_time = 4000
    time_array = np.linspace(40, max_time, 1000)

    # select the letter for the vim command
    for k, apm_file in users.items():

        datas = []
        for keyBucket in keyBuckets:
            insert_time = get_dataset_regex_licenced(
                apm_file, keyBucket, insertionTimeOnly=insertionTimeOnly
            )
            print("InsertTime", len(insert_time), keyBucket, apm_file)
            insert_time.name = k
            datas.append(insert_time)

        data2plot = pd.concat(datas, sort=False, axis=1)

        # plot asymmetrical density estimator
        # I does not assume gaussian distribution.
        fig, ax = plt.subplots()
        frames = data2plot
        for col in frames.columns:
            sweetSweetFrame = frames[col].dropna()
            n = len(sweetSweetFrame)
            ige = ImproperGammaEstimator(sweetSweetFrame, "plugin")
            ax.plot(time_array, ige(time_array), label=f"{col} - N={n}")
            ax.set_xlabel("NeoVim - InsertTime (ms)")
            ax.set_ylabel("probability density function (PDF)")
            ax.set_title(
                f"VIM command starting with '{keyBucket}' - case insensitive"
            )
            plt.legend()
        plt.show()
