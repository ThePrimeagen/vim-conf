import matplotlib.pyplot as plt
import pandas as pd

plt.style.use("dark_background")
sec2ms = 1000

# load it baby
df = pd.read_csv("apm.csv", dtype={"TotalTime": float})
totalTime = df["TotalTime"]

# must get a copy to avoid mutation of the "TotalTime" array.
insertTime = df["TotalTime"].copy()

# prepare data to ms
insertTime *= sec2ms
insertTime.name = "insertTime"
for i in range(1, 4):
    insertTime -= df[f"Stroke{i}"] * sec2ms

# plot magic
insertTime.hist(bins=100)
plt.title("vim-apm insertTime")
plt.xlabel("ms")
plt.xlim([0, 2000])
plt.show()
