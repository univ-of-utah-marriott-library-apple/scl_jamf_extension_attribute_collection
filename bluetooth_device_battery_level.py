#!/usr/bin/python

# Copyright (c) 2017 University of Utah Student Computing Labs. ################
# All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and
# its documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appears in all copies and
# that both that copyright notice and this permission notice appear
# in supporting documentation, and that the name of The University
# of Utah not be used in advertising or publicity pertaining to
# distribution of the software without specific, written prior
# permission. This software is supplied as is without expressed or
# implied warranties of any kind.
################################################################################

# bluetooth_device_battery.py #################################################
#
# A Python script monitor and report Bluetooth device battery levels.
#
#    1.0.0  2016.03.xx      Initial release tjm
#
#
#
################################################################################

# Notes ########################################################################
#
#
#
#
#
#
################################################################################

from __future__ import print_function
import subprocess
import re

def main():
    potential_devices = ["AppleBluetoothHIDKeyboard", "BNBTrackpadDevice", "BNBMouseDevice"]
    output_string = None

    bluetooth_power_state = subprocess.check_output(["defaults", "read", "/Library/Preferences/com.apple.Bluetooth.plist", "ControllerPowerState"])

    # exit if bluetooth is off
    if "0" in bluetooth_power_state:
        quit()

    for device in potential_devices:
        raw_output = subprocess.check_output(["/usr/sbin/ioreg", "-r", "-c", device])

        if raw_output == '':
            continue
        else:
            match = re.search('.*"BatteryPercent" = (.*)\n', raw_output)

            if int(match.group(1)) < 30:
                if "AppleBluetoothHIDKeyboard" in device:
                    device_output = "Bluetooth Keyboard at " + match.group(1) + "%"
                elif "BNBTrackpadDevice" in device:
                    device_output = "Bluetooth Trackpad at " + match.group(1) + "%"
                elif "BNBMouseDevice" in device:
                    device_output = "Bluetooth Mouse at " + match.group(1) + "%"
                else:
                    continue
            else:
                continue

            if output_string is None:
                output_string = device_output
            else:
                output_string = output_string + " " + device_output

    if output_string is not None:
        print("<result>" + output_string + "</result>")

if __name__ == '__main__':
    main()
