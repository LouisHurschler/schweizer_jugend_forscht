import pandas as pd
import time
import numpy as np

class TemperatureHandler:
    def __init__(self):
        self.temp = 20.
        # send the messages over mqtt too?
        
    def get_current_temperature(self) -> pd.DataFrame:
        self.temp += np.random.normal(loc=0.1,scale=0.3)
        data = pd.DataFrame({"time": [time.time()], "temperature": [self.temp]})
        return data
