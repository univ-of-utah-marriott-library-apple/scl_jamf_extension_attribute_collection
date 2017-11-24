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

# time_machine_status.py #######################################################
#
# A Python script monitor and report Time Machine settings.
#
#    1.0.0  2016.11.xx      Initial release. tjm
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
import os
import datetime

def main():
    tm_drive = "/Volumes/Time Machine"
    tm_config = False
    tm_d_avail = False

    if os.path.isdir(tm_drive):
        tm_d_avail = True

    dest_info = subprocess.check_output(['/usr/bin/tmutil', 'destinationinfo'])

    if "tmutil: No" not in dest_info:
        tm_config = True

    if tm_config:
        last_backup_raw = subprocess.check_output(['/usr/bin/tmutil', 'latestbackup'])
        last_backup_raw = last_backup_raw.split('/')[-1]
        year, month, day, time = last_backup_raw.split('-')
        time = time.split('\n')[0]
        # last_backup_date = month + day + year + ':' + time
        last_backup_date = month + "/" + day

        if tm_d_avail:
            today = datetime.date.today()
            last_backup = datetime.date(year=int(year), month=int(month), day=int(day))
            backup_elapsed = today - last_backup
            if backup_elapsed.days > 30:
                last_backup_mod = "Bad "
            else:
                last_backup_mod = "Good "

            drive_size_raw = subprocess.check_output(["/bin/df", tm_drive]).split("\n")[1].split(" ")
            drive_size_raw = [x for x in drive_size_raw if x]
            tm_d_used = drive_size_raw[4].split("%")[0]

            if int(tm_d_used) > 90:
                tm_d_mod = " Bad "
            else:
                tm_d_mod = " Good "

            tm_d_total = float(drive_size_raw[3])/(1024 ** 2)
            if tm_d_total > 1000:
                tm_d_total = tm_d_total/1024
                tm_d_total = "%0.2fT" % tm_d_total
            else:
                tm_d_total = str(int(tm_d_total)) + "G"

            return_string = last_backup_mod + last_backup_date + tm_d_mod + tm_d_used + "% free of " + tm_d_total

        else:
            return_string = 'Last Backup: ' + last_backup_date + " Not SCL drive"

    else:
        if tm_d_avail:
            return_string = 'Not configured, drive available'
        else:
            return_string = 'Not configured, no drive'

    print("<result>" + return_string + "</result>")

if __name__ == '__main__':
    main()
