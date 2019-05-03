#! /usr/bin/python

from gps import *
import time 
import os

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
timeout_counter = 0
timeout_seconds = 30

def decimal_to_degrees(dd):
   is_positive = dd >= 0
   dd = abs(dd)
   minutes,seconds = divmod(dd*3600,60)
   degrees,minutes = divmod(minutes,60)
   degrees = degrees if is_positive else -degrees
   return (degrees,minutes,seconds)

def format_location(gpsdata):
    #pull the values out
    lat = getattr(gpsdata, 'lat', 0.0)
    lon = getattr(gpsdata, 'lon', 0.0)
    alt = getattr(gpsdata, 'alt', 0)
     
    #save our bits for northing, easting, and negative altitude
    north = int(lat > 0)
    east = int(lon > 0)
    below_sea_level = int(alt < 0)

    #convert from decimal formats to degrees/minutes/seconds
    lat = decimal_to_degrees(abs(lat))
    lon = decimal_to_degrees(abs(lon))    
    
    #convert degrees and minutes to z-filled integers including the required precision
    str_lat_deg = str(int(lat[0])).zfill(2)
    str_lat_min = str(int(lat[1] * 1000)).zfill(5)
    str_lon_deg = str(int(lon[0])).zfill(3)
    str_lon_min = str(int(lon[1] * 1000)).zfill(5)
    str_alt = str(int(alt * 10)).zfill(6)

    #construct the payload as a string
    payload = ''
    payload = payload + str_lat_deg + str_lat_min + '00' + str(north) + '0'
    payload = payload + str_lon_deg + str_lon_min + '00' + str(east)
    payload = payload + str_alt + '0' + str(below_sea_level)

    #print "String payload: " + payload + "\n"

    #split the payload into bytes to be sent to rigctl
    payload = "\\0x" + "\\0x".join(a+b for a,b in zip(payload[::2], payload[1::2]))
    
    return payload

def send_update(gpsdata):
    if gpsdata['class'] == 'TPV':
	 payload = format_location(gpsdata)
	 command = "\\0xFE\\0xFE\\0x88\\0xE0\\0x1A\\0x05\\0x01\\0x86" + payload + "\\0xFD"
         command = "rigctl -m 2 w \"" + command + "\""
	 print command + "\n"
	 os.system(command)
	 raise SystemExit

try:
    while True:
	coordinates = gpsd.next()
        send_update(coordinates)

	timeout_counter = timeout_counter + 1
	if timeout_counter > timeout_seconds:
	    raise SystemError()
        time.sleep(1)

except (SystemError):
    print "No GPS fix."

except (SystemExit):
    print "Update sent."

except (KeyboardInterrupt): #when you press ctrl+c
    print "Done.\nExiting."
