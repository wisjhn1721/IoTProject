# We will use a weather API to pull historical and future data
import json
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd

# this will grab the configuration from the config.json file
def DoDoorSequence(time, file):
    # Open Door event
    file.write('Living Room,Front Door,' + time.strftime(timeFormat) + ',1,production\n')

    # Door is open for 30 seconds
    for second in range(0, 30):  # Every second that the door is open
        time += timedelta(seconds=1)

    # Door closes
    file.write('Living Room,Front Door,' + time.strftime(timeFormat) + ',0,production\n')

    # Wait 60 seconds
    for sec in range(0, 60):
        time += timedelta(seconds=1)
    return time



if __name__ == '__main__':
    f = open("demodata.csv", "w")
    timeFormat = "%m/%d/%Y %H:%M:%S"
    startTime = dt.now() - timedelta(days=7)
    endTime = dt.now()
    currentTime = startTime

    while currentTime < endTime:
        # print(currentTime)
        day = currentTime.weekday()
        # 0 - Monday ... 4 - Friday ... 6 - Sunday
        # M-F : 16 exit/enter events per day - 8 @ ~ 8am and 8 @ ~ 6pm
        # S-S : 32 exit/enter events per day - 8 @ ~ 9am, 8 @ ~ 11am, 8 @ ~ 2pm, 8 @ ~ 6pm
        # 1 is open, 0 is closed

        data = ['Living Room', 'Front Door', str(currentTime), 'production\n']
        # schema = {'location': [], 'sensor_id': [], 'time': [], 'value': [], 'dataset': []}
        line = data[0] + ',' + data[1] + ',' + str(currentTime) + ',0,production\n'

        if 0 <= day <= 4:  # M - F
            if (currentTime.hour in [8, 18]) and (currentTime.minute == 0):
                for event in range(0, 8):  # Every time a door is opened
                    currentTime = DoDoorSequence(currentTime, f)

        else:  # S - S
            if (currentTime.hour in [8, 11, 14, 18]) and (0 <= currentTime.minute <= 15):
                for event in range(0, 8):  # Every time a door is opened
                    currentTime = DoDoorSequence(currentTime, f)

        currentTime += timedelta(seconds=1)

    f.close()

