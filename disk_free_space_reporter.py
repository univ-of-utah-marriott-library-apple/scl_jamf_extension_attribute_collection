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

# disk_free_space.py ###########################################################
#
# A Python script monitor and report disk free space.
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
################################################################################

from __future__ import print_function
import subprocess

def main():
    formatted_drive_list = None
    divisor = 1953125

    raw_disks = subprocess.check_output(["/bin/df", "-lhP"])

    split_disks = raw_disks.split("\n")
    split_disks.pop(0)
    split_disks = [x for x in split_disks if x]

    for disk in iter(split_disks):
        low_space_condition = False
        split_single_disk = disk.split(" ")
        split_single_disk = [x for x in split_single_disk if x]
        disk_total = int(split_single_disk[1]) / divisor
        disk_used = int(split_single_disk[2]) / divisor
        disk_percentage = int(split_single_disk[-2].split("%")[0])
        disk_name = split_single_disk[-1].split("/")[-1]

        if disk_name == "":
            if disk_total - disk_used < 50:
                disk_name = '/'
                low_space_condition = True
        elif disk_name == "Data":
            if disk_total - disk_used < 15:
                low_space_condition = True
        else:
            if disk_percentage > 80:
                low_space_condition = True

        if low_space_condition:
            if formatted_drive_list == '':
                formatted_drive_list = formatted_drive_list + disk_name + ":" + str(disk_used) + "G/" + str(disk_total) + "G (" + str(disk_percentage) + "%)"
            else:
                formatted_drive_list = formatted_drive_list + " " + disk_name + ":" + str(disk_used) + "G/" + str(disk_total) + "G (" + str(disk_percentage) + "%)"


    print("<result>" + formatted_drive_list + "</result>")

if __name__ == '__main__':
    main()
