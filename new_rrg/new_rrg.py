from symbol import Symbol
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from colour import Color
import numpy as np


# expects
def add_price_relative(df: pd.DataFrame, relative_to: str):
    for c in df.columns:
        if c != relative_to:
            column_name = f"{c}_PR"
            df[column_name] = 100 * (df[c] / df[relative_to])
    return df


def add_rs_ratio(df: pd.DataFrame, symbols: list[str]):
    for s in symbols:
        column_name = f"{s}_RS_RATIO"
        pr_col = f"{s}_PR"
        df[column_name] = (
            100
            + (
                (df[pr_col] - df[pr_col].rolling(window=12).mean())
                / df[pr_col].rolling(window=12).std()
            )
            + 1
        )

    return df


def add_roc(df: pd.DataFrame, symbols: list[str]):
    for s in symbols:
        column_name = f"{s}_ROC"
        rs_col = f"{s}_RS_RATIO"
        df[column_name] = 100 * (df[rs_col] / df[rs_col].shift(1) - 1)

    return df


"""
101 + (
ROC-AVERAGE(last 12 ROC)
)
/
STDEV(last 12 ROC)
"""


def add_rm(df: pd.DataFrame, symbols: list[str]):
    for s in symbols:
        column_name = f"{s}_RM"
        roc_col = f"{s}_ROC"
        df[column_name] = (
            100
            + (
                (df[roc_col] - df[roc_col].rolling(window=12).mean())
                / df[roc_col].rolling(window=12).std()
            )
            + 1
        )
    return df


sp200 = Symbol(yf_symbol="^AXJO", interval="30m")
xhj = Symbol(yf_symbol="^AXHJ", interval="30m")
xij = Symbol(yf_symbol="^AXIJ", interval="30m")
xre = Symbol(yf_symbol="^AXRE", interval="30m")

symbols = ["xhj", "xij", "xre"]

combined = pd.DataFrame()
combined["asx"] = sp200.ohlc.bars.Close
combined["xhj"] = xhj.ohlc.bars.Close
combined["xij"] = xij.ohlc.bars.Close
combined["xre"] = xre.ohlc.bars.Close

combined = add_price_relative(combined, "asx")
combined = add_rs_ratio(combined, symbols)
combined = add_roc(combined, symbols)
combined = add_rm(combined, symbols)

print("banan")

# spline = make_interp_spline(combined.iloc[-15:-1].xhj_RS_RATIO, combined.iloc[-15:-1].xhj_RM)


ax1 = plt.axes()
# axis1.plot(combined.iloc[-15:-1].xhj_RS_RATIO, combined.iloc[-15:-1].xhj_RM, format="o")
# plt.show()

tail_len = 15
red = Color("maroon")
blue = Color("gray")
colours = list(red.range_to(blue, tail_len - 1))
hex_colours = [str(x) for x in colours]

x = combined.iloc[-tail_len:-1].xhj_RS_RATIO
y = combined.iloc[-tail_len:-1].xhj_RM
labels = combined.index[-tail_len:-1]

# ax1.plot(x, y, "C3", c=hex_colours, lw=1)
ax1.scatter(x, y, c=hex_colours, s=80)
ax1.axvline(c="grey", lw=1, x=100)
ax1.axhline(c="grey", lw=1, y=100)

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

lc = LineCollection(segments, colors=hex_colours)
lc.set_array(np.linspace(0, 1, len(x)))
lc.set_linewidth(2)
line = ax1.add_collection(lc)

for i in range(0, tail_len - 1):
    label = str(labels[i].time())

    plt.annotate(
        label,  # this is the text
        (x.iloc[i], y.iloc[i]),  # these are the coordinates to position the label
        textcoords="offset points",  # how to position the text
        xytext=(0, 10),  # distance from text to points (x,y)
        ha="center",
    )  # horizontal alignment can be left, right or center

plt.show()
