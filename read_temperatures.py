#! /usr/bin/env python
# read temperatures from arduino connected to serial port.
# Arduino running MAX31855_read

import sys
import datetime
import sqlite3

import serial

def open_port(port='/dev/ttyAMC0'):
    """Open serial port"""
    baudrate = 9600
    timeout = 1
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
    except serial.SerialException:
        print 'Failure to open serial port. Exiting.'
        sys.exit(1)
    return ser

def reading_loop(serial_port_obj, db_conn):
    """Read temperature values from serial port"""
    c = db_conn.cursor()
    data_pt_num = 0
    try:
        while True:
            date_time = datetime.datetime.utcnow()
            port_read = serial_port_obj.readline()
            if port_read is False or port_read is '':
                continue
            else:
                if data_pt_num < 2:    #throw away first two lines
                    data_pt_num += 1 
                    continue
                port_read = port_read.strip()
                port_read = port_read.split(',')
                t = (date_time, port_read[0],port_read[1])
                c.execute('''INSERT INTO readings VALUES (?,?,?)''', t)
                db_conn.commit()
                print t
    except KeyboardInterrupt:
        close_up(serial_port_obj, db_conn)

def close_up(serial_port_obj, db_conn):
    """Close serial port on Ctrl+C"""
    serial_port_obj.close()
    db_conn.close()
    sys.exit(0)

def ini_db():
    """Initialize a db for storing data"""
    n = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S') + '.sqlite'
    conn = sqlite3.connect(n)
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE readings
                    (datetime text, internal real, thermocouple real)''')
    except sqlite3.OperationalError:
        print 'Unable to create table with name: ' + n
        sys.exit(1)
    conn.commit()
    return conn

if __name__ == '__main__':
    if len(sys.argv) > 2:
        print 'Usage: ./'+sys.argv[0]+' [port]'
        print 'Try /dev/cu.usbmodem1421 for Mac'
        sys.exit(2)
    if len(sys.argv) == 2:
        ser = open_port(sys.argv[1])
    else:
        ser = open_port()
    conn = ini_db()
    reading_loop(ser, conn)