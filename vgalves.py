import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import pingouin as pg
from scipy import stats

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

    return totalTime


def get_dataset_regex_licenced(csv_path, list_of_cmd, insertionTimeOnly=True, strokeTiming=False):
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
        rf"^({list_of_cmd})", flags=re.IGNORECASE
    )

    filtered_df = raw_df.loc[filtered_index]
    if strokeTiming:
        time_df = filtered_df["Stroke1"] * 1000
    else:
        time_df = filtered_df["TotalTime"] * 1000

    if insertionTimeOnly and not strokeTiming:
        for i in range(1, 4):
            time_df -= raw_df[f"Stroke{i}"] * 1000

    if strokeTiming:
        for i in range(2, 4):
            time_df += raw_df[f"Stroke{i}"] * 1000


    print("Mean", csv_path, list_of_cmd, insertionTimeOnly, strokeTiming, time_df.mean())
    print("Median", csv_path, list_of_cmd, insertionTimeOnly, strokeTiming, time_df.median())

    return time_df


if __name__ == "__main__":
    # comparing insert time between users
    """
    "ThePrimeagen": [
        ["data/apm.csv", "i", "d"],#, "d", "c"],
        ["data/apm.no-cdw.csv", "i"],#, "d", "c"],
        ["data/apm.cdw.csv", "dw"]#, "cw"]
        ["data/apm.csv", "i", "d"],#, "d", "c"],
    ],
    "TJ": [
        ["data/tj.apm.csv", "i", "c"],#, "d", "c"],
        ["data/tj.apm.no-cdw.csv", "i"],#, "d", "c"],
        ["data/tj.apm.cdw.csv", "dw"]#, "cw"]
    ],

    ThePrimeagen

    || Mean i 0.0
    || Median i 0.0
    || Mean d 498.1117465775796
    || Median d 415.071680999977
    || Mean c 431.27407245391174
    || Median c 307.678101493364

    TJ
    // No statistical difference
    || Mean i 398.797514248487 // tj
    || Median i 221.24121547676498
    || Mean i 352.0407136075603 // prime
    || Median i 215.09120999507996

    // statistical difference
    || Mean data/tj.apm.csv c 394.154291518726
    || Median data/tj.apm.csv c 199.6591759962043
    || Mean data/apm.csv c 658.0412356470634
    || Median data/apm.csv c 461.91592450122505

    // Statistical Difference
    || Mean data/tj.apm.csv d 566.472934546446
    || Median data/tj.apm.csv d 336.0314434999084
    || Mean data/apm.csv d 370.5175142003057
    || Median data/apm.csv d 247.88268299744593

    // Statistical diff - stroked
    || Mean data/tj.apm.no-cdw.csv c False True 138.866599104963
    || Median data/tj.apm.no-cdw.csv c False True 134.59238099494533
    || Mean data/apm.no-cdw.csv d False True 498.1117465775796
    || Median data/apm.no-cdw.csv d False True 415.071680999977

    $(($(cat apm.csv | grep -i ^d | wc -l) * 1.0 / $(cat apm.csv | grep -i ^i | wc -l)))
    Primeagen d*** / i = 0.53470919324577859
    Primeagen c** / i = 0.12757973733583489
    Tj d*** / i = 0.12318840579710146
    Tj c** / i = 0.58333333333333337
    """
    users = {
        "Both": [
            # ["data/tj.apm.no-cdw.csv", "c"],#, "d", "c"],
            ["data/apm.no-cdw.csv", "d"],#, "d", "c"],
        ]
    }
    tjTime = get_dataset_regex_licenced(
        "data/tj.apm.no-cdw.csv", "c", True, False
    )
    primeTime = get_dataset_regex_licenced(
        "data/apm.no-cdw.csv", "d", True, False
    )

    test = stats.mannwhitneyu(tjTime, primeTime)
    print(test)

    insertionTimeOnly = False
    strokeTiming = True
    max_time = 4000
    time_array = np.linspace(40, max_time, 1000)

    # select the letter for the vim command
    for k, apm_files in users.items():

        datas = []
        for idx in range(0, len(apm_files)):
            apm_file = apm_files[idx][0]
            keyStrokes = apm_files[idx][1:]
            for sIdx in range(0, len(keyStrokes)):
                stroke = keyStrokes[sIdx]
                insert_time = get_dataset_regex_licenced(
                    apm_file, stroke, insertionTimeOnly, strokeTiming
                )
                insert_time.name = f"{k}_{stroke}"

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
                f"VIM command starting with '{k}' - case insensitive"
            )
            plt.legend()
        plt.show()
