#! /usr/bin/env python

import csv
import numpy as np
import matplotlib.pyplot as plt
import datetime

def main():
    list_ = []
    first_pt_ts = True
    with open('out.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if first_pt_ts is True:
                first_pt_ts = str_to_datetime(row[0])
            duration = str_to_datetime(row[0]) - first_pt_ts
            list_.append((duration.total_seconds(), row[1]))

    pts = np.array(list_)
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111)
    plt.title('Time v. Temperature')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Temperature (C)')
    x = pts[:,0] # timestamp
    y = pts[:,1] # internal temp
    ax.scatter(x,y)
    plt.show()

def str_to_datetime(datetime_string):
    """Convert datetime_string in db to datetime obj"""
    try:
        dt = datetime.datetime.strptime(datetime_string, '%H:%M:%S')
    except ValueError:
        dt =  datetime.datetime.max
    return dt

if __name__ == '__main__':
    main()