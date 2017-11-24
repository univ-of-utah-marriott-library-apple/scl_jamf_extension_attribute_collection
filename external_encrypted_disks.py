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

# ea_external_encrypted_disks.py ###############################################
#
# A Python script report external disks and encryption status.
#
#    1.0.0  2017.10.24      Initial release. tjm
#
################################################################################

# Notes ########################################################################
#   Example output:
#       <result>3 external drives. 1 encrypted.</result>
#
#   Offline encrypted (ejected, but still attached) drives will cause odd results.
#   Checking for physical and external is probably overkill...
#
################################################################################

from __future__ import print_function
import subprocess

def main():
    raw_disklist = subprocess.check_output(["/usr/sbin/diskutil", "list"])
    raw_disklist = raw_disklist.split("\n")

    external_disks = 0
    encrypted_disks = 0

    for item in raw_disklist:
        if "/dev/disk" in item and "physical" in item and "external" in item:
            external_disks += 1
        elif "Encrypted" in item:
            encrypted_disks += 1

    if external_disks >= 2:
        print("<result>" + str(external_disks) + " external drives. " + str(encrypted_disks) + " encrypted.</result>")
    elif external_disks:
        print("<result>External Drive Present. " + str(encrypted_disks) + " encrypted.</result>")

if __name__ == '__main__':
    main()
