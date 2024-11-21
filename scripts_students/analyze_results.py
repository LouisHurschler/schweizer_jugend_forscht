import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# TODO:
# add relay state??? For that, it should be added in simulation??? For that, it should be added in simulation
# think about other ways of analyzing results, excel? jupyter notebook?


def plot_results(
    temp_data: pd.DataFrame,
    box_data: pd.DataFrame,
    target_temp: float,
    threshold: float,
):

    # use matplotlib or similar libraries to plot results
    fig, ax1 = plt.subplots()

    times = pd.to_datetime(temp_data["time"], unit="s")
    temps = temp_data["temperature"]
    ax1.plot(times, temps, label="temperture [C°]")

    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    ax2 = ax1.twinx()

    ax2.plot(
        pd.to_datetime(box_data["time"], unit="s"),
        box_data["power"],
        label="Power [kW]",
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
    plot_results(temp_data, box_data, target_temp, threshold)
    # analyze results further.
    # possible questions:
    # what is the percentage of times the temperature is in the threshold?
    # What is the total power consumed? What is the mean power consumed per time?
    # What is the efficiency of the boiler (for example, calculate how much power is needed to heat the water to some degree and then compare with heat capacity of water)
    # What is the smallest threshold you could have achieved? are there different strategies which would be able to achieve smaller threshold
    # what would happen if somebody changed the water to cold water?
    ...


if __name__ == "__main__":
    analyze_results()
