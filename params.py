#! /usr/bin/python3 -u
################################################################################
#
# Params.py - Rev 1.0
# Copyright (C) 2021 by Joseph B. Attili, aa2il AT arrl DOT net
#
# Command line param parser for satellite predictions.
#
################################################################################
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
################################################################################

import os
from rig_io.ft_tables import SATELLITE_LIST,CONNECTIONS,SAT_RIGS
import argparse
from settings import *

################################################################################

# Structure to contain processing params
class PARAMS:
    def __init__(self):

        # Process command line args
        arg_proc = argparse.ArgumentParser()
        arg_proc.add_argument("-n", help="No. Days",type=int,default=30)
        arg_proc.add_argument('-update', action='store_true',\
                              help='Update TLE Data from Internet')
        arg_proc.add_argument("-grid", help="Grid Square",
                              type=str,default=None)
        arg_proc.add_argument("-rig", help="Connection Type",
                              type=str,default=["ANY"],nargs='+',
                              choices=CONNECTIONS+['NONE']+SAT_RIGS)
        arg_proc.add_argument("-port", help="Connection Port",
                              type=int,default=0)
        arg_proc.add_argument("-rotor", help="Rotor connection Type",
                              type=str,default="NONE",
                              choices=['HAMLIB','NONE'])
        arg_proc.add_argument("-port2", help="Rotor onnection Port",
                              type=int,default=0)
        arg_proc.add_argument("-sat", help="Sat to Track",
                              type=str,default=None)
        arg_proc.add_argument('-sdr', action='store_true',
                              help='Command SDR also')
        
        args = arg_proc.parse_args()
        self.NDAYS2     = args.n
        self.UPDATE_TLE = args.update
        if args.sat:
            self.sat_name  = args.sat.upper()
        else:
            self.sat_name  = None

        self.connection    = args.rig[0]
        if len(args.rig)>=2:
            self.rig       = args.rig[1]
        else:
            self.rig       = None
        self.PORT          = args.port
            
        self.ROTOR_CONNECTION = args.rotor
        self.PORT2            = args.port2
        
        self.USE_SDR          = args.sdr
        self.SDR_CONNECTION   = 'HAMLIB'
        self.PORT3            = 4575            # Needs to be same port SDR is listening on
        
        # Read config file
        self.RCFILE=os.path.expanduser("~/.satrc")
        self.SETTINGS=None
        try:
            with open(self.RCFILE) as json_data_file:
                self.SETTINGS = json.load(json_data_file)
        except:
            print(self.RCFILE,' not found - need call!\n')
            s=SETTINGS(None,self)
            while not self.SETTINGS:
                try:
                    s.win.update()
                except:
                    pass
                time.sleep(.01)
            print('Settings:',self.SETTINGS)

        self.MY_GRID    = args.grid
        if self.MY_GRID==None:
            self.MY_GRID = self.SETTINGS['MY_GRID']
        