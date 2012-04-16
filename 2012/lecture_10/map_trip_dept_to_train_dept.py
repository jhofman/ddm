'''This file maps trips from the MTA GTFS to (train, departure), for Tuesdays, assuming that the trains are running on time.'''

import csv
import sys
import datetime

#route_id,service_id,trip_id,trip_headsign,direction_id,block_id,shape_id

def trip_to_train(f):
    """
    >>> f = open('trips.txt')
    >>> out = trip_to_train(f)
    >>> out['A20111204WKD_000800_1..S03R']
    ('1','1')
    """
    out = {}
    d = csv.DictReader(f)
    for row in d:
        trip_id = row['trip_id']
        route_id = row['route_id']
        direction = row['direction_id']
        if trip_id in out:
            raise IndexError
        out[trip_id] = route_id, direction
    return out

def mins_since_midnight(s):
    """
    >>> mins_since_midnight("00:08:00")
    8
    >>> mins_since_midnight("24:08:00")
    8
    """
    hr,m,sec = map(int,s.split(':'))
    hr = hr%24
    s2 = ':'.join(map(str,[hr,m,sec]))
    dt = datetime.datetime.strptime(s2, "%H:%M:%S")
    return dt.hour*60+dt.minute

#{'pickup_type': '0', 'stop_headsign': '', 'shape_dist_traveled': '', 'arrival_time': '00:19:00', 'stop_sequence': '9', 'stop_id': '111S', 'drop_off_type': '0', 'trip_id': 'A20111204WKD_000800_1..S03R', 'departure_time': '00:19:00'}
def main():
    t_to_t = trip_to_train(open('trips.txt'))
    d = csv.DictReader(sys.stdin)
    for row in d:
        if row['stop_sequence'] != '1' or 'WKD' not in row['trip_id']:
            continue
        route_id, direction = t_to_t[row['trip_id']]
        dept = row['departure_time']
        print "\t".join(map(str,[route_id, direction, mins_since_midnight(dept)]))
        
    
if __name__ == "__main__":
    main()
