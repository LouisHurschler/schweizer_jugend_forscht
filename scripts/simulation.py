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
from PIL import Image, ImageTk
import datetime as dt
import matplotlib.dates as mdates


# BoilerSimulationApp class handles the GUI setup and functionality for a boiler simulation.


class BoilerSimulationApp:
    def __init__(self, root):
        # general configuration
        self.background = "white"
        self.root = root
        self.root.configure(background=self.background)
        self.font_size = 20

        # create a 9x9 grid for layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)
        self.root.grid_columnconfigure(2, weight=1)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=2)
        self.root.grid_rowconfigure(2, weight=1)

        # Define the path to the current directory for loading resources
        self.current_path = os.path.dirname(os.path.abspath(__file__))

        # Initialize handlers for temperature and device controls
        self.temperature_handler = TemperatureHandler()
        self.box_handler = BoxHandler()

        # Default relay state
        self.relay_state = "1"

        # Set up fullscreen window to match screen dimensions
        screen_width = self.root.winfo_screenwidth()  # Get screen width
        screen_height = self.root.winfo_screenheight()  # Get screen height
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        # Load and display schweizerjugendforscht logo image with scaling
        self.image_frame = tk.Frame(self.root, background=self.background)
        self.image_frame.grid(row=0, column=0, columnspan=3)
        self.original_image = Image.open(
            os.path.join(self.current_path, "data/Schweizer_Jugend_forscht_logo.png")
        )
        original_width, original_height = self.original_image.size
        # adjust this factor such that it fits nicely into the frame
        scaling_factor = min(
            screen_width / (original_width * 10.0),
            screen_height / (original_height * 10.0),
        )
        # Convert the PIL image to a Tkinter-compatible image
        self.image = ImageTk.PhotoImage(
            self.original_image.resize(
                (
                    int(original_width * scaling_factor),
                    int(original_height * scaling_factor),
                )
            )
        )

        self.image_label = tk.Label(
            self.image_frame,
            image=self.image,
            compound="left",
            background=self.background,
        )  # what does compound = "left" mean? how can i have the picture on the left?
        self.image_label.grid(row=0, column=0)

        # Define frames for layout organization
        self.left_frame = tk.Frame(self.root, background=self.background)
        self.left_frame.grid(row=1, column=0)
        self.middle_frame = tk.Frame(self.root, background=self.background)
        self.middle_frame.grid(row=1, column=1)
        self.right_frame = tk.Frame(self.root, background=self.background)
        self.right_frame.grid(row=1, column=2)

        # Heater control slider in the left frame
        self.label_heater = tk.Label(
            self.left_frame, text="Switch Heater manually", background=self.background
        )
        self.slider_heater = tk.Scale(
            self.left_frame,
            from_=0,
            to=1,
            orient=tk.HORIZONTAL,
            background=self.background,
            highlightthickness=0,
            command=lambda value: self.toggle_device(value),
        )
        self.label_heater.grid(row=0, column=0)
        self.slider_heater.grid(row=1, column=0)

        # Initialize data storage for plots and relay states
        self.box_data = pd.DataFrame()
        self.temperature_data = pd.DataFrame()
        self.relay_states = pd.DataFrame(columns=["time", "state"])

        # Add initial relay state with current time
        default = pd.DataFrame(
            {"time": [dt.datetime.now()], "state": [self.relay_state]}
        )
        self.relay_states = pd.concat([self.relay_states, default], ignore_index=True)

        # Setup data points for plotting and checkbuttons to control display options
        self.stuff_to_plot = [
            "voltage",
            "current",
            "power",
            "apparent_energy",
            "power_factor",
        ]
        self.checkbutton_states = [tk.IntVar(value=1) for _ in self.stuff_to_plot]
        self.temp_state = tk.IntVar(value=1)
        self.checkbuttons = [
            tk.Checkbutton(
                self.right_frame,
                variable=var,
                text=name,
                background=self.background,
                highlightthickness=0,
            )
            for var, name in zip(self.checkbutton_states, self.stuff_to_plot)
        ]
        self.checkbutton_temp = tk.Checkbutton(
            self.right_frame,
            variable=self.temp_state,
            text="temperature",
            background=self.background,
            highlightthickness=0,
        )
        for i, checkbutton in enumerate(self.checkbuttons):
            checkbutton.grid(row=i, column=0)
        self.checkbutton_temp.grid(row=len(self.checkbuttons), column=0)

        # Initialize matplotlib figure and canvas
        self.fig, (self.ax, self.axtemp) = plt.subplots(2, 1, sharex=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.middle_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.canvas.draw()

        # set initial device state (off)
        self.toggle_device(0)

    # Toggles the device state based on slider input
    def toggle_device(self, value: int):
        if self.relay_state != value:
            self.box_handler.toggle_device(value)
            new_entry = pd.DataFrame({"time": [dt.datetime.now()], "state": [value]})
            self.relay_states = pd.concat(
                [self.relay_states, new_entry], ignore_index=True
            )
            self.relay_state = value
            # set the slider if it is toggled in code
            self.slider_heater.set(value)

    # Updates the plot with the latest data
    def update_plot(self):
        self.box_data = self.box_handler.get_data()
        self.temperature_data = pd.concat(
            [self.temperature_data, self.temperature_handler.get_current_temperature()],
            ignore_index=True,
        )

        # Save data to CSV files
        self.box_data.to_csv(self.current_path + "/data/res_box.csv", index=False)
        self.temperature_data.to_csv(
            self.current_path + "/data/res_temp.csv", index=False
        )

        # this code gets called every second. Your task is to add logic here to reach a constant temperature
        ############################# Enter logic here #############################
        # toggles device randomly for now
        # if np.random.normal() > 0:
        #     self.toggle_device(1)
        # else:
        #     self.toggle_device(0)
        ############################# Enter logic here #############################

        self.redraw_canvas()
        # This function gets called every second. Do stuff here to steer the water temperature
        self.root.after(1000, self.update_plot)

    # Clears and redraws the matplotlib canvas with current data
    def redraw_canvas(self):
        self.ax.clear()
        self.axtemp.clear()

        max_value = 0.0
        if "time" in self.temperature_data.keys():
            last_temperature_measurement = self.temperature_data["time"].iloc[0]
        else:
            last_temperature_measurement = dt.datetime.now()
        for i, keyword in enumerate(self.stuff_to_plot):
            if (
                self.checkbutton_states[i].get() == 1
                and keyword in self.box_data.keys()
            ):
                self.ax.plot(
                    pd.to_datetime(self.box_data["time"], unit="s"),
                    self.box_data[keyword],
                    label=keyword,
                )
                max_value = max(max_value, max(self.box_data[keyword]))
            else:
                if self.checkbutton_states[i].get() == 1 and not self.box_data.empty:
                    print(
                        f"{keyword} not in self.box_data.keys: {self.box_data.keys()}"
                    )
        self.highlight_relay_states(self.ax, max_value)

        # Plot temperature data
        i = len(self.stuff_to_plot)
        if "temperature" in self.temperature_data and self.temp_state.get() == 1:
            self.axtemp.plot(
                pd.to_datetime(self.temperature_data["time"], unit="s"),
                self.temperature_data["temperature"],
                label="temperature",
            )
            self.highlight_relay_states(
                self.axtemp, max(self.temperature_data["temperature"])
            )

        # This step is done to "clip off" old values, such that we only see the last min in the plot
        # get_xlim get the values of the x-axis in days,
        # therefore to enable max one minute of plotting substract 1/(24*60)
        current_xlim = self.fig.gca().get_xlim()
        self.ax.set_xlim(
            [
                max(current_xlim[0], current_xlim[1] - 1.0 / (24.0 * 60.0)),
                current_xlim[1],
            ]
        )

        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        self.ax.xaxis.set_major_locator(plt.MaxNLocator(4))

        # update the new canvas
        self.canvas.draw()

    # Highlights relay states on the plot
    def highlight_relay_states(self, ax, max_value):
        alphavalue = 0.25
        last_time = None
        last_state = None
        for time, state in zip(self.relay_states["time"], self.relay_states["state"]):
            if last_time:
                if int(state) == 0:
                    color = "green"
                else:
                    color = "red"
                ax.fill_betweenx(
                    [0, max_value],
                    last_time,
                    time,
                    color=color,
                    alpha=alphavalue,
                    zorder=1,
                )
            last_time = time
        if int(self.relay_state) == 0:
            color = "red"
        else:
            color = "green"
        ax.fill_betweenx(
            [0, max_value],
            last_time,
            dt.datetime.now(),
            color=color,
            alpha=alphavalue,
            zorder=1,
        )


def main():
    root = tk.Tk()
    app = BoilerSimulationApp(root)
    app.update_plot()
    root.mainloop()


if __name__ == "__main__":
    main()
