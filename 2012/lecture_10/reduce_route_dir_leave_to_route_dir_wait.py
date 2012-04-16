'''This program takes the output of the mapper and produces a wait time for every (route, direction, hour of day)'''

import sys
import csv
import itertools
import numpy as np

def make_diffs(ns):
    ns = np.asarray(ns)
    return np.median(np.diff(ns)/2)

def parse(times):
    '''expects sorted list of times'''
    g = itertools.groupby(times, lambda x: x/60)
    for hour, hr_times in g:
        hr_times = list(hr_times)
        yield hour, make_diffs(hr_times)

def main():
    c = csv.reader(sys.stdin, delimiter='\t')
    g = itertools.groupby(c, lambda x: (x[0],x[1]))
    for key,rows in g:
        depts = []
        for row in rows:
            depts.append(row[-1])
        for hour, wait in parse(sorted(map(int,depts))):
            print key, hour, wait


if __name__ == "__main__":
    main()
