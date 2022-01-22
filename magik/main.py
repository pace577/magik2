#!/usr/bin/env python3

import argparse
from userprofile import Profile

def main():
    # Initialize profile
    p = Profile()
    p.initialize_config_from_files()

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="sub-command help")

    # watch command
    watch_parser = subparsers.add_parser('watch', help='watch help')
    watch_parser.set_defaults(func=p.attend_current_slot)

    # open command
    open_parser = subparsers.add_parser('open', help='open help')
    open_parser.add_argument('class')
    open_parser.add_argument('link_type')
    watch_parser.set_defaults()
    # parser.add_argument('echo', help="echos that variable in the console")
    # parser.add_argument('-v', '--verbosity', help="increase output verbosity", action="store_true")
    args = parser.parse_args()
    print(args)
    # if args.verbosity:
    #     print("Verbosity turned on")

if __name__ == '__main__':
    main()
