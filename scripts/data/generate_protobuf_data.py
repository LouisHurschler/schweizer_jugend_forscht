from scripts.hardware_tests.switch_mock_up.data.TimeSpanLog_pb2 import TimeSpanLog
from google.protobuf.timestamp_pb2 import Timestamp
import time

def generate_data():
    log = TimeSpanLog()

    # populate fields; this is just an example
    log.id = 1
    log.type = TimeSpanLog.type_1_second
    log.timestamp_from.GetCurrentTime()
    log.timestamp_to.GetCurrentTime()
    log.L1_power_factor_average = 1.0
    # ... populate other fields as required ...

    return log.SerializeToString()

if __name__ == "__main__":
    data = generate_data()
    with open('serialized_data.bin', 'wb') as f:
        f.write(data)
