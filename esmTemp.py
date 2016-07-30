import os
import glob
import time
import subprocess
import statistics
import decimal

# Based off of https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software



# Read the file representing the temperature sensor
def read_temp_raw():

    # Find the file-mapped location of the temperature sensor
    try:
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
    except IndexError:
        return None


    catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')
    return lines

# Convert the information from raw reads to degrees f
def read_temp():
    temp_f = []
    # Read the temperature twice, ensure that the readings are consistent
    for i in range(0,3):
        lines = read_temp_raw()
        if lines == None:
            return 0
        # Convert the data to temperature count
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f.append( temp_c * 9.0 / 5.0 + 32.0)
    # Check to see if standard deviation is less than 2 degrees f
    if statistics.stdev(temp_f) > 2:
        # Return nothing if the data is invalid
        return None
    else:
        # Otherwise, return the median of the measured temperatures
        return float(round(decimal.Decimal(statistics.median_grouped(temp_f)),2))

def setup():
    # Setup the temperature system
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

