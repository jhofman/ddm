#!/bin/bash

# download google transit data from the nyc mta
# note: substitute 'wget' for 'curl -O' if need be
[ -f google_transit.zip ] || curl -O http://www.mta.info/developers/data/nyct/subway/google_transit.zip

# extract stop_times and trips files
[ -f stop_times.txt ] || unzip google_transit.zip stop_times.txt
[ -f trips.txt ] || unzip google_transit.zip trips.txt

# compute wait times and output in wait_times.txt
# format: line, direction, hour, minutes
echo `date` "computing wait times"
cat stop_times.txt | \
    python map_trip_dept_to_train_dept.py | \
    sort | \
    python reduce_route_dir_leave_to_route_dir_wait.py > wait_times.txt
echo `date` "done"
