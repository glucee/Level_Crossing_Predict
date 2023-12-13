import json
from datetime import datetime, timedelta
# from pyodide.http import open_url # for PyScript
import urllib.request

stations = [("bns", "Barnes"),   #train station name, you can find it at
            ("mtl", "Mortlake")] #https://raw.githubusercontent.com/jpsingleton/Huxley2/master/station_codes.csv
Access_Token = "" #You will need to add your access token
close_window = 2 # the closure time windows in minutes 
# check the next three trains between station 0 to station 1
URLs=[ "https://huxley2.azurewebsites.net/departures/"+stations[0][0]+"/to/"+stations[1][0]+"/3/?accessToken="+Access_Token,
"https://huxley2.azurewebsites.net/departures/"+stations[1][0]+"/to/"+stations[0][0]+"/3/?accessToken="+Access_Token]

time_table = [] # store the departure times between two stations
window_flag = [] # check if two trains are in the closure windows: 1 in the closure window, 0: not
time_format = "%H:%M"
current_time = datetime.now().replace(second=0, microsecond=0)


for url in URLs:
    # response = open_url(url) # for PyScript
    response = urllib.request.urlopen(url)
    trains = json.load(response)["trainServices"]
    for train in trains:
        departure = datetime.strptime(train["std"], time_format)
        departure = departure.replace(current_time.year, current_time.month, current_time.day)
        if departure > current_time: # predict for the future
            time_table.append(departure)

time_table = sorted(time_table)

for i in range(0, len(time_table)-1):
    if time_table[i + 1] - time_table[i] <= timedelta(minutes=close_window):
        window_flag.append(1)
    else:
        window_flag.append(0)
window_flag.append(0)

print("Predicted Closed Time: {} - {}".format(stations[0][1], stations[1][1]))
if time_table[0] - current_time <= timedelta(minutes=close_window):
    print(current_time.time(), (time_table[0]+timedelta(minutes=1)).time())

index = 0
while (index < len(time_table)):
    begin = time_table[index]
    while (window_flag[index] == 1):
        index += 1
    end = time_table[index] + timedelta(minutes=close_window/2)
    index += 1
    print(begin.time(), end.time())
