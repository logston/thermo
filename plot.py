#! ../bin/python

''' This module creates a matplotlib scatter plot with thermocouple 
data from a sqlite3 database. The module checks every second for updates
to the database table and updates the scatter plot accordingly.'''

import os
import sqlite3
import time
import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime

def main():
    """Watch database and update plot appropriately"""
    db_dir = 'data/'

    file_list = os.listdir(db_dir)
    file_name = file_list[-1]   # Get the most recent db file
    print file_name
    conn = sqlite3.connect(db_dir + file_name)
    c = conn.cursor()

    plt.ion()
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111)
    plt.title('Time v. Temperature')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Temperature (C)')

    first_pt_ts = True
    t_list = []
    sql_ = '''SELECT * FROM readings'''
    
    while True:
        new_pt_list = []
        new_pts = None
        for row in c.execute(sql_):
            if first_pt_ts is True:
                t_list.append(row)
                first_pt_ts = str_to_datetime(row[0])
                sql_ = '''SELECT * FROM readings ORDER BY timestamp DESC LIMIT 10'''
                first_pt = (0, row[1], row[2])
                pts = np.array(first_pt)
                print first_pt
            if row not in t_list:
                t_list.append(row)
                duration = str_to_datetime(row[0]) - first_pt_ts
                new_pt_list.append((duration.total_seconds(), row[1], row[2]))
                print new_pt_list[-1]
        if new_pt_list:
            new_pts = np.array(new_pt_list)
            pts = np.vstack((pts, new_pts))
        x = pts[:,0] # timestamp
        y = pts[:,1] # internal temp
        z = pts[:,2] # thermocouple
        ax.scatter(x,y)
        plt.draw()
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            plt.close('all')
            conn.close()
            sys.exit(0)

def str_to_datetime(datetime_string):
    """Convert datetime_string in db to datetime obj"""
    try:
        dt = datetime.datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        dt =  datetime.datetime.max
    return dt

if __name__ == '__main__':
    main()