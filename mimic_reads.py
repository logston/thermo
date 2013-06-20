#! ../bin/python

'''This module automatically inserts fictitious temperature readings into a
database in order to mimic a thermocouple taking periodic readings.'''

import sys
import datetime
import sqlite3
import time
import random
import os
import math

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

    tp = 0
    while True:
        date_time = datetime.datetime.utcnow()
        port_read = readline(tp) # Comes in form ddd.dd,ddd.dd\n
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
            time.sleep(1)
        except KeyboardInterrupt:
            conn.close()
            sys.exit(0)
        tp += 1

def readline(tp):
    """Return a fake data point from a fake thermocouple. 'internal,thermocouple\n'"""
    internal = math.cos(tp/100) + random.uniform(-0.1,0.1) + 5 
    thermocouple = math.sqrt(tp) + random.uniform(-1,1)
    return str(round(internal, 2)) + ',' + str(round(thermocouple, 2)) + '\n'

if __name__ == '__main__':
    main()