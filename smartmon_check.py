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

# SMART_EA.py #################################################
#
# A Python script monitor and report SMART details from disks.
#
#    1.0.0  2016.03.xx      Initial release. tjm
#    1.1.0  2016.12.07      report devices with SMART disabled. tjm
#    1.2.0  2017.04.07      Adjusted method of drive discovery. tjm
#                           No longer checking external drives.
#
#
################################################################################

# Notes ########################################################################
#
# Requires smartmon tools
#
# External SMART report unavailable in MacOS
#
# A checked drive will have a character showing it's status:
#
#   .   SMART status is okay
#   #   The drive number will appear if a SMART error is detected
#   ?   If smartmon couldn't open the device
#
################################################################################

from __future__ import print_function
import subprocess

def main():
    ouput_disklist = ""

    raw_disklist = subprocess.check_output(["/usr/sbin/diskutil", "list",])
    raw_disklist = raw_disklist.split("\n")

    disk_list = []
    for item in raw_disklist:
        if "/dev/disk" in item and "physical" in item and "external" not in item:
            item = item.split(" (")
            disk_list.append(item[0])

    for index, drive_name in enumerate(disk_list):
        try:
            check_smart = subprocess.check_output(["/usr/local/sbin/smartctl", "-a", drive_name])
            if "SMART Disabled." in check_smart:
                # could turn smart on here...
                ouput_disklist = ouput_disklist + "X"
            else:
                smart_output = subprocess.check_call(["/usr/local/sbin/smartctl", "-H", "--quietmode=errorsonly", drive_name])
                # print smart_output
                if smart_output == 0:
                    ouput_disklist = ouput_disklist + "."
                else:
                    ouput_disklist = ouput_disklist + str(index)
        except Exception as exception_message:
            # print(exception_message)
            ouput_disklist = ouput_disklist + "?"

    print("<result>" + ouput_disklist + "</result>")

if __name__ == '__main__':
    main()
