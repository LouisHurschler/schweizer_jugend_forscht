import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
from temperature_handler import TemperatureHandler
from box_handler import BoxHandler




class BoilerSimulationApp:
    def __init__(self, root):
        self.root = root
        # general
        self.font_size = 20
        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_columnconfigure(1, weight = 3)
        self.root.grid_columnconfigure(2, weight = 1)

        self.current_path = os.path.dirname(os.path.abspath(__file__))

        self.temperature_handler = TemperatureHandler()
        self.box_handler = BoxHandler()

        self.relay_state = 0



        self.left_frame = tk.Frame(self.root)
        self.left_frame.grid(row=0, column=0)
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.grid(row=0, column=1)
        self.right_frame = tk.Frame(self.root)
        self.right_frame.grid(row=0, column=2)


        self.label_heater = tk.Label(self.left_frame, text='Heater')
        self.slider_heater = tk.Scale(self.left_frame, from_=0, to=1, orient=tk.HORIZONTAL,
        command=lambda value:
        self.toggle_device(value))
        self.label_heater.grid(row=0, column=0)
        self.slider_heater.grid(row=1, column=0)


        self.box_data = pd.DataFrame()
        self.temperature_data = pd.DataFrame()

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.middle_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.canvas.draw()
        self.stuff_to_plot = ["L1_voltage", "L1_current", "L1_power", "L1_apparent_energy",
                              "L1_power_factor"]
        self.checkbutton_states = [tk.IntVar() for _ in self.stuff_to_plot]
        self.temp_state = tk.IntVar()
        self.checkbuttons = [tk.Checkbutton(self.right_frame, variable = var, text = name) for
                             var, name in zip(self.checkbutton_states, self.stuff_to_plot)]
        self.checkbutton_temp = tk.Checkbutton(self.right_frame, variable = self.temp_state,
                                               text = "temperature")
        for i, checkbutton in enumerate(self.checkbuttons):
            checkbutton.grid(row=i, column=0)
        self.checkbutton_temp.grid(row=len(self.checkbuttons), column = 0)

    def toggle_device(self, value: int):
        if self.relay_state != value:
            self.box_handler.toggle_device(value)

    def update_plot(self):
        self.box_data = self.box_handler.get_data()
        self.temperature_data = pd.concat([self.temperature_data,
            self.temperature_handler.get_current_temperature()], ignore_index=True)
        self.redraw_canvas()
        # This function gets called every second. Do stuff here to steer the water temperature



        self.root.after(1000, self.update_plot)

    def redraw_canvas(self):
        self.ax.clear()

        for i, keyword in enumerate(self.stuff_to_plot):
            if self.checkbutton_states[i].get() == 1 and keyword in self.box_data.keys():
                self.ax.plot(self.box_data["time"], self.box_data[keyword], label=keyword)
            else:
                if self.checkbutton_states[i].get() == 0:
                    print(f'{keyword} not in self.box_data.keys')
        i = len(self.stuff_to_plot)
        if ("temperature" in self.temperature_data and
                                   self.temp_state.get() == 1):
            self.ax.plot(self.temperature_data["time"], self.temperature_data["temperature"],
                     label="temperature")
        self.canvas.draw()
        # print("box_data:")
        # print(self.box_data)

        self.box_data.to_csv(self.current_path + "/data/res_box.csv", index=False)
        self.temperature_data.to_csv(self.current_path + "/data/res_temp.csv", index=False)





def main():
    root = tk.Tk()
    app = BoilerSimulationApp(root)
    app.update_plot()
    root.mainloop()





if __name__ == "__main__":
    main()
