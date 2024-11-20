import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
from temperature_handler import TemperatureHandler
from box_handler import BoxHandler
from PIL import Image, ImageTk
import datetime as dt
import matplotlib.dates as mdates


# convert timestamps (seconds since January 1, 1970) to datetime objects
# note that the timestamp object shows the time measured in utc.
# to convert to MET (UTC +1), we have to add one hour
def convert_timestamp_to_MET_datetimes(timestamps: pd.Series) -> list:
    times = pd.to_datetime(timestamps, unit="s") + pd.Timedelta(hours=1)
    return times


# BoilerSimulationApp class handles the GUI setup and functionality for a boiler simulation.
class BoilerSimulationApp:

    def __init__(self, root):
        # general configuration
        self.setup_general_config(root)

        # Initialize handlers for temperature and device controls
        self.temperature_handler = TemperatureHandler()
        self.box_handler = BoxHandler()

        # Default relay state
        self.relay_state = "1"
        # Initialize data storage for plots and relay states
        self.box_data = pd.DataFrame()
        self.temperature_data = pd.DataFrame()
        self.relay_states = pd.DataFrame(
            {"time": [dt.datetime.now()], "state": [self.relay_state]}
        )

        # setup slider to manually control heater
        self.setup_heater_slider()

        # setup plotting
        self.setup_plotting()

        # setup plotting
        self.setup_checkbuttons()

        # set initial device state (off)
        self.toggle_device(0)

    def setup_general_config(self, root):
        """Configures the main application window and sets initial parameters."""

        self.background = "white"
        self.root = root
        self.root.configure(background=self.background)
        self.font_size = 12

        self.main_frame = tk.Frame(
            root,
            background=self.background,
            padx=30,
            pady=30,
        )

        # Define the path to the current directory for loading resources
        self.current_path = os.path.dirname(os.path.abspath(__file__))

        # create a 3x2 grid for layout
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=2)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=2)
        self.main_frame.grid_rowconfigure(2, weight=2)
        self.main_frame.pack(expand=True, fill="both")

        # Define frames for layout organization
        self.slider_frame = tk.Frame(
            self.main_frame,
            background=self.background,
        )
        self.slider_frame.grid(row=1, column=0)
        self.plot_frame = tk.Frame(self.main_frame, background=self.background)
        self.plot_frame.grid(row=1, column=1, rowspan=2)
        self.checkbutton_frame = tk.Frame(
            self.main_frame, background=self.background
        )
        self.checkbutton_frame.grid(row=2, column=0)

        # Set up fullscreen window to match screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(
            f"{self.screen_width}x{self.screen_height}+1000+1000"
        )

        # Load and display schweizerjugendforscht logo image with scaling
        self.image_frame_left = tk.Frame(
            self.main_frame, background=self.background
        )
        self.image_frame_left.grid(row=0, column=0, sticky="wn")
        self.image_frame_right = tk.Frame(
            self.main_frame, background=self.background
        )
        self.image_frame_right.grid(row=0, column=1, sticky="en")
        self.original_image_sjf = Image.open(
            os.path.join(
                self.current_path, "data/Schweizer_Jugend_forscht_logo.png"
            )
        )
        self.original_image_hslu = Image.open(
            os.path.join(
                self.current_path, "data/HSLU_Logo_DE_Schwarz_rgb.png"
            )
        )
        original_width_sjf, original_height_sjf = self.original_image_sjf.size
        original_width_hslu, original_height_hslu = (
            self.original_image_hslu.size
        )
        new_image_height = int(self.screen_height / 20.0)
        # adjust this factor such that it fits nicely into the frame
        # Convert the PIL image to a Tkinter-compatible image
        self.image_sjf = ImageTk.PhotoImage(
            self.original_image_sjf.resize(
                (
                    int(
                        original_width_sjf
                        * new_image_height
                        / original_height_sjf
                    ),
                    new_image_height,
                )
            )
        )

        self.image_label = tk.Label(
            self.image_frame_right,
            image=self.image_sjf,
            background=self.background,
        )
        self.image_label.pack()
        # Convert the PIL image to a Tkinter-compatible image
        self.image_hslu = ImageTk.PhotoImage(
            self.original_image_hslu.resize(
                (
                    int(
                        original_width_hslu
                        * new_image_height
                        / original_height_hslu
                    ),
                    new_image_height,
                )
            )
        )

        self.image_label_hslu = tk.Label(
            self.image_frame_left,
            image=self.image_hslu,
            background=self.background,
        )
        self.image_label_hslu.pack()
        self.main_frame.pack()

    def setup_heater_slider(self):

        # Heater control slider in the left frame
        self.label_heater = tk.Label(
            self.slider_frame,
            text="Heater",
            font=("Arial", self.font_size, "bold"),
            background=self.background,
        )
        self.slider_heater = tk.Scale(
            self.slider_frame,
            from_=0,
            to=1,
            font=("Arial", self.font_size, "bold"),
            orient=tk.HORIZONTAL,
            # troughcolor=self.background,
            background=self.background,
            highlightthickness=0,
            command=lambda value: self.toggle_device(value),
        )
        self.label_heater.pack()
        self.slider_heater.pack()

    def setup_checkbuttons(self):
        self.checkbutton_states = [
            tk.IntVar(value=1) for _ in self.stuff_to_plot
        ]
        self.temp_state = tk.IntVar(value=1)
        self.checkbuttons = [
            tk.Checkbutton(
                self.checkbutton_frame,
                font=("Arial", self.font_size),
                variable=var,
                text=label,
                background=self.background,
                highlightthickness=0,
                anchor="w",
            ).pack(anchor="w")
            for var, (_, label) in zip(
                self.checkbutton_states, self.stuff_to_plot
            )
        ]
        self.checkbutton_temp = tk.Checkbutton(
            self.checkbutton_frame,
            font=("Arial", self.font_size),
            variable=self.temp_state,
            text="temperature [C°]",
            background=self.background,
            highlightthickness=0,
        ).pack(anchor="w")

    def setup_plotting(self):
        # Setup data points for plotting and checkbuttons to control display options
        self.stuff_to_plot = [
            ("voltage", "voltage [V]"),
            ("current", "current [A]"),
            ("power", "power [kW]"),
            ("power_factor", "power factor"),
        ]
        # Initialize matplotlib figure and canvas
        self.fig, (self.ax, self.axtemp) = plt.subplots(
            2, 1, sharex=True, figsize=(14, 10)
        )
        # set background colors for plot
        self.fig.set_facecolor(self.background)
        self.ax.set_facecolor(self.background)
        self.axtemp.set_facecolor(self.background)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.canvas.draw()

    # Toggles the device state based on slider input
    def toggle_device(self, value: int):
        if self.relay_state != value:
            self.box_handler.toggle_device(value)
            new_entry = pd.DataFrame(
                {"time": [dt.datetime.now()], "state": [value]}
            )
            self.relay_states = pd.concat(
                [self.relay_states, new_entry], ignore_index=True
            )
            self.relay_state = value
            # set the slider if it is toggled in code
            self.slider_heater.set(value)

    # Updates the plot with the latest data
    # you can add additional information, for example to stop at the next timestep
    def update_plot(self, additional_information=None):
        self.box_data = self.box_handler.get_data()
        self.temperature_data = (
            self.temperature_handler.get_current_temperature()
        )

        # Save data to CSV files
        self.box_data.to_csv(
            self.current_path + "/data/res_box.csv", index=False
        )
        self.temperature_data.to_csv(
            self.current_path + "/data/res_temp.csv", index=False
        )

        # this code gets called every second. Your task is to add logic here to reach a constant temperature
        ############################# Enter logic here #############################
        # test logic which heats iff temp < target_temp - 0.9 threshold
        target_temp = 45
        threshold = 3
        if additional_information == "stop":
            self.toggle_device("0")
            additional_information = 3
        if additional_information != None and additional_information != "stop":
            if additional_information <= 0:
                additional_information = None
            else:
                additional_information -= 1

        if not self.temperature_data.empty:
            temp = self.temperature_data["temperature"].iloc[-1]
            if len(self.temperature_data["temperature"]) > 1:
                last_temp = self.temperature_data["temperature"].iloc[-2]
            else:
                last_temp = target_temp
        else:
            temp = target_temp
            last_temp = target_temp
        if temp < target_temp - 0.9 * threshold and int(self.relay_state) == 0:
            self.toggle_device("1")
        if temp > target_temp - 0.9 * threshold and int(self.relay_state) == 1:
            self.toggle_device("0")
        if (
            target_temp - threshold < temp < target_temp
            and last_temp > temp
            and int(self.relay_state) == 0
        ):
            if additional_information == None:
                self.toggle_device("1")
                additional_information = "stop"

        print(additional_information, temp)
        ############################# Enter logic here #############################

        self.redraw_canvas()
        # This function gets called every second. Do stuff here to steer the water temperature
        self.root.after(
            1000,
            self.update_plot,
            additional_information,
        )

    # Clears and redraws the matplotlib canvas with current data
    def redraw_canvas(self):
        self.ax.clear()
        self.axtemp.clear()

        max_value = 0.0
        if "time" in self.temperature_data.keys():
            last_temperature_measurement = self.temperature_data["time"].iloc[
                0
            ]
        else:
            last_temperature_measurement = dt.datetime.now()
        for i, (keyword, label) in enumerate(self.stuff_to_plot):
            if (
                self.checkbutton_states[i].get() == 1
                and keyword in self.box_data.keys()
            ):
                self.ax.plot(
                    convert_timestamp_to_MET_datetimes(self.box_data["time"]),
                    self.box_data[keyword],
                    label=label,
                )
                max_value = max(max_value, max(self.box_data[keyword]))
            else:
                if (
                    self.checkbutton_states[i].get() == 1
                    and not self.box_data.empty
                ):
                    print(
                        f"{keyword} not in self.box_data.keys: {self.box_data.keys()}"
                    )
        self.highlight_relay_states(self.ax, max_value)

        # Plot temperature data
        i = len(self.stuff_to_plot)
        if (
            "temperature" in self.temperature_data
            and self.temp_state.get() == 1
        ):
            self.axtemp.plot(
                convert_timestamp_to_MET_datetimes(
                    self.temperature_data["time"]
                ),
                self.temperature_data["temperature"],
                label="temperature [C°]",
            )
            self.highlight_relay_states(
                self.axtemp, max(self.temperature_data["temperature"])
            )

        # configure dates and shown region
        self.configure_plot_axis()

        # update the new canvas
        self.canvas.draw()

    # Highlights relay states on the plot
    def highlight_relay_states(self, ax, max_value):
        alphavalue = 0.25
        last_time = None
        last_state = None
        for time, state in zip(
            self.relay_states["time"], self.relay_states["state"]
        ):
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

    def configure_plot_axis(self):
        # This step is done to "clip off" old values, such that we only see the last min in the plot
        # get_xlim get the values of the x-axis in days,
        # therefore to enable max two minutes of plotting substract 1/(24*30)
        current_xlim = self.fig.gca().get_xlim()

        # add ten seconds on the right side for nicer plots
        xlim_end = current_xlim[1]
        xlim_start = max(current_xlim[0], xlim_end - 1.0 / (24 * 30))

        # self.ax.set_xlim([xlim_start, xlim_end])

        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        self.ax.xaxis.set_major_locator(plt.MaxNLocator(4))
        self.ax.legend()
        self.axtemp.legend()


def main():
    root = tk.Tk()
    app = BoilerSimulationApp(root)
    app.update_plot()
    root.mainloop()


if __name__ == "__main__":
    main()
