# Icom IC-7100 GPS Position Updater

This script uses a CI-V command to update the GPS position in the radio.

## Requirements

- Icom IC-7100 Radio
- Raspberry Pi with a GPS device and Python 2.7.9
- Connected with USB cable

Make sure gpsd is installed and configure it to to read from your GPS.

```sudo apt-get install gpsd gpsd-clients python-gps```

You should see live position data when running ```gpsmon```

## Build Hamlib

Install the tools needed to build hamlib.  The version from apt doesn't support the IC-7100

```sudo apt-get install -y autoconf automake libtool build-essential pkg-config texinfo```

Build hamlib from the source

```git clone https://git.code.sf.net/p/hamlib/code hamlib-code```

```cd hamlib-code```

```autoreconf -i```

```./configure```

```make```

```sudo make install```

Once that's in place, you should be able to run ```rigctl```

## Clone

Clone this repo

```git clone https://github.com/mcleanra/ic7100-gps-updater```

```cd ./ic7100-gps-updater```

```
sudo python ./update_gps.py
```
> Update sent.

## Add a job to do it every 5 minutes

```sudo crontab -e```

Add this line at the bottom of the file and save

```
*/5 * * * * python /home/pi/ic7100-gps-updater/update_gps.py
```

## Caveats

This thing assumes your radio is on /dev/ttyUSB0.  If not then just change that line in the script
