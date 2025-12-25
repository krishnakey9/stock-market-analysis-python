import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec


def plot_dashboard(df):
    fig = plt.figure(figsize=(14, 10), constrained_layout=True)

    # Grid: 4 rows, 2 columns
    gs = GridSpec(4, 2, height_ratios=[3, 1, 1, 1], figure=fig)

    ax_price = fig.add_subplot(gs[0, :])
    ax_volume = fig.add_subplot(gs[1, :], sharex=ax_price)
    ax_rsi = fig.add_subplot(gs[2, 0], sharex=ax_price)
    ax_macd = fig.add_subplot(gs[2, 1], sharex=ax_price)

    # -------- PRICE --------
    ax_price.plot(df["Date"], df["Close"], label="Close", color="black", alpha=0.9)
    ax_price.plot(df["Date"], df["SMA_20"], label="SMA 20", color="blue")
    ax_price.plot(df["Date"], df["SMA_50"], label="SMA 50", color="orange")
    ax_price.plot(df["Date"], df["EMA_20"], label="EMA 20", color="red")

    ax_price.set_title("Stock Price Analysis (Raw Data)")
    ax_price.legend()
    ax_price.grid(True, alpha=0.3)

    # -------- VOLUME --------
    ax_volume.bar(
        df["Date"],
        df["Volume"],
        color="gray",
        alpha=0.6,
        width=1
    )
    ax_volume.set_title("Volume")
    ax_volume.set_ylabel("Volume")
    ax_volume.grid(True, alpha=0.3)

    # -------- RSI --------
    ax_rsi.plot(df["Date"], df["RSI"], color="purple")
    ax_rsi.axhline(70, linestyle="--", color="red")
    ax_rsi.axhline(30, linestyle="--", color="green")
    ax_rsi.set_ylim(0, 100)
    ax_rsi.set_title("RSI")
    ax_rsi.grid(True, alpha=0.3)

    # -------- MACD --------
    ax_macd.plot(df["Date"], df["MACD"], label="MACD", color="green")
    ax_macd.plot(df["Date"], df["Signal"], label="Signal", color="red")
    ax_macd.set_title("MACD")
    ax_macd.legend()
    ax_macd.grid(True, alpha=0.3)

    # -------- DATE AXIS (CLEAN & ADAPTIVE) --------
    locator = mdates.AutoDateLocator(minticks=5, maxticks=10)
    formatter = mdates.ConciseDateFormatter(locator)

    ax_price.xaxis.set_major_locator(locator)
    ax_price.xaxis.set_major_formatter(formatter)

    ax_price.set_xlim(df["Date"].min(), df["Date"].max())
    ax_price.margins(x=0)

    plt.show()
