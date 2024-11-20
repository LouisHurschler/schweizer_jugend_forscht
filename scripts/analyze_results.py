import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_results(
    temp_data: pd.DataFrame,
    box_data: pd.DataFrame,
    target_temp: float,
    threshold: float,
):

    fig, ax1 = plt.subplots()

    times = pd.to_datetime(temp_data["time"], unit="s")
    max_temp = max(temp_data["temperature"])
    min_temp = min(temp_data["temperature"])
    print(min_temp)
    print(max_temp)

    ax1.plot(times, temp_data["temperature"], label="temperature [C°]")
    if (
        max_temp > target_temp - threshold
        and min_temp < target_temp + threshold
    ):
        ax1.fill_between(
            times,
            max(target_temp - threshold, min_temp),
            min(target_temp + threshold, max_temp),
            color="green",
            alpha=0.5,
        )

    if min_temp < target_temp - threshold:
        ax1.fill_between(
            times,
            min_temp,
            min(target_temp - threshold, max_temp),
            color="red",
            alpha=0.5,
        )

    if max_temp > target_temp + threshold:
        ax1.fill_between(
            times,
            target_temp + threshold,
            max_temp,
            color="red",
            alpha=0.5,
        )

    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    ax2 = ax1.twinx()

    to_plot = pd.to_datetime(box_data["time"], unit="s") > times.iloc[0]

    ax2.plot(
        pd.to_datetime(box_data["time"], unit="s")[to_plot],
        box_data["power"][to_plot],
        label="power [kW]",
        color="orange",
    )
    ax1.set_xlabel("time")
    ax1.set_ylabel("Temperature [C°]")
    ax2.set_ylabel("Power [kW]")

    fig.legend()
    plt.show()


def analyze_results():
    # the main goal is to minimize the mean power whilst maximizing (at best 100%) the percentage
    # in threshold
    target_temp = 45.0
    threshold = 3.0
    current_path = os.path.dirname(os.path.abspath(__file__))
    # windows
    # box_data = pd.read_csv(current_path + "\\data\\res_box.csv")
    # temp_data = pd.read_csv(current_path + "\\data\\res_temp.csv")
    # linux

    # get data from files
    box_data = pd.read_csv(current_path + "/data/res_box.csv")
    temp_data = pd.read_csv(current_path + "/data/res_temp.csv")

    temperature_reached = temp_data["temperature"][
        temp_data["temperature"] >= target_temp - threshold
    ]
    if not temperature_reached.empty:
        first_timestep_to_reach_threshold = temp_data["temperature"][
            temp_data["temperature"] >= target_temp - threshold
        ].index[0]
        relevant_data = temp_data["temperature"][
            first_timestep_to_reach_threshold:
        ]
        first_timestep = temp_data["time"][first_timestep_to_reach_threshold]
        percentage_in_threshold = np.mean(
            [
                target_temp - threshold <= temp <= target_temp + threshold
                for temp in relevant_data
            ]
        )
        print(f"percentage in threshold: {percentage_in_threshold}")
    else:
        print("target temperature never reached!!!")

    if len(box_data["time"]) >= 2:
        time_diff_box = box_data["time"].iloc[-1] - box_data["time"].iloc[0]

        mean_current = box_data["current"].sum() / time_diff_box
        mean_voltage = box_data["voltage"].sum() / time_diff_box
        mean_power = box_data["power"].sum() / time_diff_box
        print(f"mean current: {mean_current}")
        print(f"mean voltage: {mean_voltage}")
        print(f"mean power: {mean_power}")
        print(mean_current * mean_voltage)
        print(f"mean temperature: {temp_data["temperature"].mean()}")
    else:
        print("too less box datapoints to calculate mean")
    plot_results(temp_data, box_data, target_temp, threshold)


if __name__ == "__main__":
    analyze_results()
