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


class BoilerSimulationApp:
    def __init__(self, root):
        self.background = "white"
        self.root = root
        self.root.configure(background=self.background)
        # general
        self.font_size = 20

        # create a 9x9 grid to plot apps
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)
        self.root.grid_columnconfigure(2, weight=1)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=2)
        self.root.grid_rowconfigure(2, weight=1)

        self.current_path = os.path.dirname(os.path.abspath(__file__))

        # setup handlers
        self.temperature_handler = TemperatureHandler()
        self.box_handler = BoxHandler()

        # default relay state
        self.relay_state = "1"

        # setup fullscreen
        screen_width = self.root.winfo_screenwidth()  # Get screen width
        screen_height = self.root.winfo_screenheight()  # Get screen height
        self.root.geometry(
            f"{screen_width}x{screen_height}+0+0"
        )  # Set window size to screen size

        # show schweizerjugendforscht image
        self.image_frame = tk.Frame(self.root, background=self.background)
        self.image_frame.grid(row=0, column=0, columnspan=3)
        self.original_image = Image.open(
            os.path.join(self.current_path, "data/Schweizer_Jugend_forscht_logo.png")
        )  # Open the image with PIL
        original_width, original_height = self.original_image.size
        scaling_factor = min(
            screen_width / (original_width * 10.0),
            screen_height / (original_height * 10.0),
        )
        self.image = ImageTk.PhotoImage(
            self.original_image.resize(
                (
                    int(original_width * scaling_factor),
                    int(original_height * scaling_factor),
                )
            )
        )  # Convert the PIL image to a Tkinter-compatible image

        self.image_label = tk.Label(
            self.image_frame,
            image=self.image,
            compound="left",
            background=self.background,
        )  # what does compound = "left" mean? how can i have the picture on the left?
        self.image_label.grid(row=0, column=0)

        self.left_frame = tk.Frame(self.root, background=self.background)
        self.left_frame.grid(row=1, column=0)
        self.middle_frame = tk.Frame(self.root, background=self.background)
        self.middle_frame.grid(row=1, column=1)
        self.right_frame = tk.Frame(self.root, background=self.background)
        self.right_frame.grid(row=1, column=2)

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

        self.box_data = pd.DataFrame()
        self.temperature_data = pd.DataFrame()

        self.relay_states = pd.DataFrame(columns=["time", "state"])

        default = pd.DataFrame(
            {"time": [dt.datetime.now()], "state": [self.relay_state]}
        )
        self.relay_states = pd.concat([self.relay_states, default], ignore_index=True)

        self.stuff_to_plot = [
            "L1_voltage",
            "L1_current",
            "L1_power",
            "L1_apparent_energy",
            "L1_power_factor",
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

        # setup plot
        self.fig, (self.ax, self.axtemp) = plt.subplots(2, 1, sharex=True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.middle_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.canvas.draw()
        # default out
        self.toggle_device(0)

    def toggle_device(self, value: int):
        print(value)
        if self.relay_state != value:
            self.box_handler.toggle_device(value)
            new_entry = pd.DataFrame({"time": [dt.datetime.now()], "state": [value]})
            self.relay_states = pd.concat(
                [self.relay_states, new_entry], ignore_index=True
            )
            self.relay_state = value

    def update_plot(self):
        self.box_data = self.box_handler.get_data()
        self.temperature_data = pd.concat(
            [self.temperature_data, self.temperature_handler.get_current_temperature()],
            ignore_index=True,
        )
        self.redraw_canvas()
        # This function gets called every second. Do stuff here to steer the water temperature
        self.root.after(1000, self.update_plot)

    def redraw_canvas(self):
        self.ax.clear()
        self.axtemp.clear()
        max_datapoints = 100

        # plot energy data
        something_plotted = False
        max_value = 0.0
        for i, keyword in enumerate(self.stuff_to_plot):
            if (
                self.checkbutton_states[i].get() == 1
                and keyword in self.box_data.keys()
            ):
                something_plotted = True
                if len(self.box_data["time"]) <= max_datapoints:
                    self.ax.plot(
                        pd.to_datetime(self.box_data["time"], unit="s"),
                        self.box_data[keyword],
                        label=keyword,
                    )
                    max_value = max(max_value, max(self.box_data[keyword]))
                else:
                    self.ax.plot(
                        pd.to_datetime(
                            self.box_data["time"][-max_datapoints:], unit="s"
                        ),
                        self.box_data[keyword][-max_datapoints:],
                        label=keyword,
                    )
            else:
                if self.checkbutton_states[i].get() == 1 and not self.box_data.empty:
                    print(
                        f"{keyword} not in self.box_data.keys: {self.box_data.keys()}"
                    )
        if something_plotted:
            self.ax.set_visible(True)
            self.plot_relay_states(self.ax, max_value)
        else:
            self.ax.set_visible(False)

        # plot temperature
        i = len(self.stuff_to_plot)
        if "temperature" in self.temperature_data and self.temp_state.get() == 1:
            self.axtemp.set_visible(True)
            if len(self.temperature_data["time"]) <= max_datapoints:
                self.axtemp.plot(
                    pd.to_datetime(self.temperature_data["time"], unit="s"),
                    self.temperature_data["temperature"],
                    label="temperature",
                )
            else:
                self.axtemp.plot(
                    pd.to_datetime(
                        self.temperature_data["time"][-max_datapoints:], unit="s"
                    ),
                    self.temperature_data["temperature"][-max_datapoints:],
                    label="temperature",
                )
            self.plot_relay_states(
                self.axtemp, max(self.temperature_data["temperature"])
            )
        else:
            self.axtemp.set_visible(False)

        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        self.ax.xaxis.set_major_locator(plt.MaxNLocator(4))
        self.canvas.draw()
        # print("box_data:")
        # print(self.box_data)

        self.box_data.to_csv(self.current_path + "/data/res_box.csv", index=False)
        self.temperature_data.to_csv(
            self.current_path + "/data/res_temp.csv", index=False
        )

    def plot_relay_states(self, ax, max_value):
        alphavalue = 0.25
        last_time = None
        last_state = None
        for time, state in zip(self.relay_states["time"], self.relay_states["state"]):
            time = time - dt.timedelta(seconds=60 * 60)
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
            dt.datetime.now() - dt.timedelta(seconds=60 * 60),
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
