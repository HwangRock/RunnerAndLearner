import matplotlib.pyplot as plt
import pandas as pd
from ex_running import controller
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def main():
    ctrl = controller.Controller()
    records = ctrl.preprocess()
    df = pd.DataFrame(records)

    dates = df["date"]
    rx = range(len(dates))

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(rx, df["time_sec"], marker="o")
    axes[0].set_title("Workout Time by Date")
    axes[0].set_ylabel("Time (sec)")

    for i, y, label in zip(rx, df["time_sec"], df["name"]):
        axes[0].annotate(label, (i, y),
                         textcoords="offset points",
                         xytext=(0, 5),
                         ha='center')

    axes[1].plot(rx, df["kcal"], marker="o", color="black")
    axes[1].set_title("Calories by Date")
    axes[1].set_ylabel("kcal")

    for i, y, label in zip(rx, df["kcal"], df["name"]):
        axes[1].annotate(label, (i, y),
                         textcoords="offset points",
                         xytext=(0, 5),
                         ha='center')

    for ax in axes:
        ax.set_xlabel("Date")
        ax.set_xticks(rx)
        ax.set_xticklabels(dates, rotation=45)

    plt.tight_layout()
    plt.show()

    predict = ctrl.predict_next()
    print("next predicted data: ", predict)


if __name__ == "__main__":
    main()
