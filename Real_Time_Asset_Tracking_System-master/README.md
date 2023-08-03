# Realtime Asset Tracking System
Updates till now:

Savatzki.py has the following changes:

--> take data directly from the raw data collected as excel file but after converting it into .xlsx file

--> filter it without any interpolation

--> separate the raw data into 4 dataframes each containing the data from each beacon

--> filter them individually and output as 4 excel files each containing the output data of each beacon


Savatzki Flowchart has been added as a word file.

Reduced the number of times filtered to 4500. Now runtime for savatzki.py is 8.423.

Unnecessary code for debugging purposes has been removed.

Filtered data iteration 1 was done with 2 beacons on different plane but all at 1m distance

Filtered Data iteration 2,3,4 was done with all beacons on same plane at 1m distance. 

The rssi comparison is done by taking the average of rssi values of each iteration. 
