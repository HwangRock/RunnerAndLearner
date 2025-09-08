import matplotlib.pyplot as plt
import pandas as pd
import controller


def main():
    ctrl = controller.Controller()
    records = ctrl.preprocess()
    df = pd.DataFrame(records)

    dates = df["date"]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    axes[0, 0].plot(dates, df["time_sec"], marker="o")
    axes[0, 0].set_title("Workout Time by Date")
    axes[0, 0].set_xlabel("Date")
    axes[0, 0].set_ylabel("Time (sec)")

    axes[0, 1].plot(dates, df["velocity_mps"], marker="o", color="red")
    axes[0, 1].set_title("Velocity by Date")
    axes[0, 1].set_xlabel("Date")
    axes[0, 1].set_ylabel("Velocity (m/s)")

    axes[1, 0].plot(dates, df["distance_km"], marker="o", color="green")
    axes[1, 0].set_title("Distance by Date")
    axes[1, 0].set_xlabel("Date")
    axes[1, 0].set_ylabel("Distance (km)")

    axes[1, 1].plot(dates, df["kcal"], marker="o", color="black")
    axes[1, 1].set_title("Calories by Date")
    axes[1, 1].set_xlabel("Date")
    axes[1, 1].set_ylabel("kcal")

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    predict = ctrl.predict_next()
    print("next predicted data: ", predict)


if __name__ == "__main__":
    main()
