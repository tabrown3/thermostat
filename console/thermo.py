import argparse
from curtemp_handler import curtemp_handler
from targettemp_handler import targettemp_handler

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# Move the below handlers into modules as needed
def tolerance_handler(args):
    print(args)

def mode_handler(args):
    print(args)

def status_handler(args):
    print(args)

def fan_handler(args):
    print(args)

curtemp_parser = subparsers.add_parser("curtemp") # utility for working with the thermostat's current temperature reading
curtemp_mutex_group = curtemp_parser.add_mutually_exclusive_group()
curtemp_mutex_group.add_argument("--send", type=int)
curtemp_mutex_group.add_argument("--force", type=int)
curtemp_mutex_group.add_argument("--reset", action="store_true")
curtemp_parser.set_defaults(func=curtemp_handler)

targettemp_parser = subparsers.add_parser("targettemp") # utility for setting (ac/heat) target temperature
curtemp_mutex_group2 = targettemp_parser.add_mutually_exclusive_group()
curtemp_mutex_group2.add_argument("--ac", type=int)
curtemp_mutex_group2.add_argument("--heat", type=int)
targettemp_parser.set_defaults(func=targettemp_handler)

tolerance_parser = subparsers.add_parser("tolerance") # utility for setting the target temp tolerance (e.g. +/- 2 degrees, etc)
tolerance_parser.set_defaults(func=tolerance_handler)

mode_parser = subparsers.add_parser("mode") # utility for working with the thermostat's current mode (ac/heat/off)
mode_parser.set_defaults(func=mode_handler)

status_parser = subparsers.add_parser("status") # utility for turning the unit (ac or heater) on, off, or auto
status_parser.set_defaults(func=status_handler)

fan_parser = subparsers.add_parser("fan") # utility for turning the fan on or auto
fan_parser.set_defaults(func=fan_handler)

ns = parser.parse_args()
ns.func(ns)