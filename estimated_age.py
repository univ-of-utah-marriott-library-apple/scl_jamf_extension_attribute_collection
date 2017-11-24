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

# estimated_age.py #############################################################
#
# A Python script to report estimated age of machine.
#
#    1.0.0  2016.11.xx      Initial release. tjm
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
    # http://www.macrumors.com/2010/04/16/apple-tweaks-serial-number-format-with-new-macbook-pro/
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
    return year_time

def cvt_days(days):
    years, days = divmod(days, 365)
    if years == 0:
        return "< 1 Year"
    elif years == 1:
        if days < 180:
            return "1 Year"
        else:
            return "2 Years"
    else:
        if days < 180:
            return "%i Years" % years
        else:
            return "%i Years" % (years + 1)

def main():
    serial_raw = subprocess.check_output(['system_profiler', 'SPHardwareDataType'])
    serial_raw = re.search('Serial.*: (.*)\n', serial_raw)
    serial_number = serial_raw.group(1)

    est_date = offline_estimated_manufacture(serial_number)
    today = datetime.date.today()

    diff = today - est_date
    diff_days = diff.days

    print("<result>" + cvt_days(diff_days) + "</result>")

if __name__ == '__main__':
    main()
