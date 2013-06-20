#! /usr/local/bin/python

'''This module automatically inserts fictitious temperature readings into a
database in order to mimic a thermocouple taking periodic readings.'''

import sys
import datetime
import sqlite3
import time
import random
import os
import math
import csv

def main():
    """This method controls insertion of fake data into a database."""
    db_dir = 'data/'
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    n = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S') + '.sqlite'
    try:
        conn = sqlite3.connect(db_dir + n)
    except sqlite3.OperationalError:
        print 'Unable to create database: ' + n
        sys.exit(1)
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE readings
                    (timestamp TEXT, internal FLOAT, thermocouple FLOAT)''')
    except sqlite3.OperationalError:
        print 'Unable to create table with name: ' + n
        sys.exit(1)
    conn.commit()

    csvfile = open('out.csv', 'r')
    csvreader = csv.reader(csvfile)
    tp = 0
    date_time = datetime.datetime.utcnow()
    while True:
        date_time = date_time + datetime.timedelta(seconds=1)
        try:
            port_read = readline(csvreader.next()) # Comes in form ddd.dd,ddd.dd\n
        except:
            print 'Could not read line/row ' + str(tp)
            conn.close()
            sys.exit(1)
        port_read = port_read.strip()
        port_read = port_read.split(',')
        t = (date_time, port_read[0], port_read[1])
        i = 0
        while i < 3:
            try:
                c.execute('''INSERT INTO readings VALUES (?,?,?)''', t)
                conn.commit()
                break
            except:
                i += 1
        print t
        try:
            pass
        except KeyboardInterrupt:
            conn.close()
            sys.exit(0)
        tp += 1

def readline(row):
    thermocouple = row[1]
    return str(0) + ',' + str(thermocouple) + '\n'

if __name__ == '__main__':
    main()