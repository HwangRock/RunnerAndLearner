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

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(dates, df["time_sec"], marker="o")
    axes[0].set_title("Workout Time by Date")
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel("Time (sec)")
    for x, y, label in zip(dates, df["time_sec"], df["name"]):
        axes[0].annotate(label, (x, y),
                         textcoords="offset points",
                         xytext=(0, 5),
                         ha='center')

    axes[1].plot(dates, df["kcal"], marker="o", color="black")
    axes[1].set_title("Calories by Date")
    axes[1].set_xlabel("Date")
    axes[1].set_ylabel("kcal")
    axes[1].plot(dates, df["kcal"], marker="o", color="black")
    axes[1].set_title("Calories by Date")
    axes[1].set_xlabel("Date")
    axes[1].set_ylabel("kcal")
    for x, y, label in zip(dates, df["kcal"], df["name"]):
        axes[1].annotate(label, (x, y),
                         textcoords="offset points",
                         xytext=(0, 5),
                         ha='center')

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    predict = ctrl.predict_next()
    print("next predicted data: ", predict)


if __name__ == "__main__":
    main()
