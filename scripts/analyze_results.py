import pandas as pd
import os
import numpy as np

def analyze_results():
    # the main goal is to minimize the mean power whilst maximizing (at best 100%) the percentage
    # in threshold
    target_temp = 26
    threshold=2
    current_path = os.path.dirname(os.path.abspath(__file__))
    box_data = pd.read_csv(current_path + "\\data\\res_box.csv")
    temp_data = pd.read_csv(current_path + "\\data\\res_temp.csv")
    first_timestep_to_reach_threshold = temp_data["temperature"][temp_data["temperature"] >=
                                                                 target_temp - threshold].index[0]
    relevant_data = temp_data["temperature"][first_timestep_to_reach_threshold:]
    first_timestep = temp_data["time"][first_timestep_to_reach_threshold]
    percentage_in_threshold = np.mean([target_temp - threshold <= temp <= target_temp + threshold
                                       for temp in relevant_data])
    print(f"percentage in threshold: {percentage_in_threshold}")

    time_diff_box = box_data["time"].iloc[-1] - box_data["time"].iloc[0]
    mean_temp = temp_data["temperature"].mean()

    mean_current = box_data["L1_current"].sum() / time_diff_box
    mean_voltage = box_data["L1_voltage"].sum() / time_diff_box
    mean_power = box_data["L1_power"].sum() / time_diff_box
    print(mean_current)
    print(mean_voltage)
    print(mean_power)
    print(mean_current * mean_voltage)
    # TODO: calculate total power, power per time or other useful data

if __name__ == "__main__":
    analyze_results()
