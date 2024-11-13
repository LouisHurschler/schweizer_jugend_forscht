import pandas as pd
import os
import numpy as np


def analyze_results():
    # the main goal is to minimize the mean power whilst maximizing (at best 100%) the percentage
    # in threshold
    target_temp = 26
    threshold = 2
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
        relevant_data = temp_data["temperature"][first_timestep_to_reach_threshold:]
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
    else:
        print("too less box datapoints to calculate mean")


if __name__ == "__main__":
    analyze_results()
