#!/usr/bin/python

# Copyright (c) 2020 University of Utah Student Computing Labs. ################
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

# estimated_date_of__manufacture.py ############################################
#
# A Python script to report estimated manufacture date.
#
#    1.0.0  2016.03.xx      Initial release tjm
#
#    1.0.1  2020.02.19      Hack to fix year loop. tjm
#
#
################################################################################

# Notes ########################################################################
#
# This script uses aggressively borrowed code from:
#
#   https://github.com/pudquick/pyMacWarranty/blob/master/getwarranty.py
#
#
################################################################################

from __future__ import print_function
import subprocess
import re
import datetime

def offline_estimated_manufacture(serial):
    est_date = u''
    if 10 < len(serial) < 13:
        if len(serial) == 11:
            # Old format
            year = serial[2].lower()
            est_year = 2000 + '   3456789012'.index(year)
            week = int(serial[3:5]) - 1
            year_time = datetime.date(year=est_year, month=1, day=1)
            if week:
                week_dif = datetime.timedelta(weeks=week)
                year_time += week_dif
            est_date = u'' + year_time.strftime('%Y-%m-%d')
        else:
            # New format
            alpha_year = 'cdfghjklmnpqrstvwxyz'
            year = serial[3].lower()
            est_year = 2010 + (alpha_year.index(year) / 2)

            #
            # This is a crazy hack. T2's appeared in 2018, pretty sure all machines have them by 2020.
            if t2_present() and est_year < 2018:
                est_year += 10

            # 1st or 2nd half of the year
            est_half = alpha_year.index(year) % 2
            week = serial[4].lower()
            alpha_week = ' 123456789cdfghjklmnpqrtvwxy'
            est_week = alpha_week.index(week) + (est_half * 26) - 1
            year_time = datetime.date(year=est_year, month=1, day=1)
            if est_week:
                week_dif = datetime.timedelta(weeks=est_week)
                year_time += week_dif
            est_date = u'' + year_time.strftime('%Y-%m-%d')
    return est_date

def t2_present():

    t2_raw = subprocess.check_output(['system_profiler', 'SPiBridgeDataType'])
    return "Apple T2 Security Chip" in t2_raw


def main():
    serial_raw = subprocess.check_output(['system_profiler', 'SPHardwareDataType'])
    serial_raw = re.search('Serial.*: (.*)\n', serial_raw)
    serial_number = serial_raw.group(1)

    est_date = offline_estimated_manufacture(serial_number)

    print("<result>" + est_date + "</result>")

if __name__ == '__main__':
    main()
