#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  deb_bintray.py
#
#  Copyright 2017 Mark Clarkstone <git@markclarkstone.co.uk>
#  See LICENSE.
#
import glob
import os
from apt import debfile


def deb_details(filename, distsep='~'):
    """Returns package information.

       :param filename: debian file to return info from.
       :param distsep: distro separator.
    """
    distsep = distsep or '~'
    deb = debfile.DebPackage(filename)
    return deb._sections['Version'].split(distsep, 2)

def deb_list():
    """Returns all matching deb files from current directory."""
    pattern = os.path.join(os.getcwd(), '*.deb')
    return glob.glob(pattern)

def main(args):
    try:
        name_hint = args[1]
    except IndexError:
        print('Package name hint required')
        return 1

    matches = deb_list()
    err = False
    for package in matches:
        if not name_hint in package:
            print('Skipping {}'.format(package))
            continue
        try:
            version, dist = deb_details(package)
        except ValueError:
            print('Skipping "{}" version info error'.format(package))
            err = True
            continue

    return int(err)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
