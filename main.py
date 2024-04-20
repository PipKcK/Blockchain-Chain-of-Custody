#!/usr/bin/env python3

import argparse
import sys
import os

import init as INIT
import CONSTANTS as CONS
import add as ADD
import checkout as CHECKOUT
import checkin as CHECKIN
import remove as REMOVE


# from icecream import ic

#Authors: ZebraCatPenguin: Ujjwal, Wejdan

#bchoc add -c case_id -i item_id [-i item_id ...] -c creator -p password(creator’s)
#bchoc checkout -i item_id -p password
#bchoc checkin -i item_id -p password
#bchoc show cases -p password
#bchoc show items -c case_id -p password
#bchoc show history [-c case_id] [-i item_id] [-n num_entries] [-r] -p password
#bchoc remove -i item_id -y reason -p password(creator’s)
#bchoc init
#bchoc verify

def main():

    parser = argparse.ArgumentParser(prog='main')
    subparsers = parser.add_subparsers(dest='command')

    #bchoc add -c case_id -i item_id [-i item_id ...] -c creator -p password(creator’s)
    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('-c', '--case_id', required=True, help='Case ID')
    parser_add.add_argument('-i', '--item_id', action='append', required=True, help='Item ID')
    parser_add.add_argument('-g', '--creator', required=True, help='Creator')
    parser_add.add_argument('-p', '--password', required=True, help='Password')

    #bchoc checkout -i item_id -p password
    parser_checkout = subparsers.add_parser('checkout')
    parser_checkout.add_argument('-i', '--item_id', required=True, help='Item ID')
    parser_checkout.add_argument('-p', '--password', required=True, help='Password')

    #bchoc checkin -i item_id -p password
    parser_checkin = subparsers.add_parser('checkin')
    parser_checkin.add_argument('-i', '--item_id', required=True, help='Item ID')
    parser_checkin.add_argument('-p', '--password', required=True, help='Password')

    #bchoc show cases -p password
    #bchoc show items -c case_id -p password
    #bchoc show history [-c case_id] [-i item_id] [-n num_entries] [-r] -p password
    parser_show = subparsers.add_parser('show')
    show_subparsers = parser_show.add_subparsers(dest='show_command')

    #bchoc show cases -p password
    parser_show_cases = show_subparsers.add_parser('cases')
    parser_show_cases.add_argument('-p', '--password', required=True, help='Password')

    #bchoc show items -c case_id -p password
    parser_show_items = show_subparsers.add_parser('items')
    parser_show_items.add_argument('-c', '--case_id', required=True, help='Case ID')
    parser_show_items.add_argument('-p', '--password', required=True, help='Password')

    #bchoc show history [-c case_id] [-i item_id] [-n num_entries] [-r] -p password
    parser_show_history = show_subparsers.add_parser('history')
    parser_show_history.add_argument('-c', '--case_id', required=False, help='Case ID')
    parser_show_history.add_argument('-i', '--item_id', required=False, help='Item ID')
    parser_show_history.add_argument('-n', '--num_entries', required=False, help='Number of entries')
    parser_show_history.add_argument('-r', '--reverse', action='store_true', required=False, help='Reverse')
    parser_show_history.add_argument('-p', '--password', required=True, help='Password')

    #bchoc remove -i item_id -y reason -p password(creator’s)
    parser_remove = subparsers.add_parser('remove')
    parser_remove.add_argument('-i', '--item_id', required=True, help='Item ID')
    parser_remove.add_argument('-y', '--reason', required=True, help='Reason')
    parser_remove.add_argument('-p', '--password', required=True, help='Password')

    # bchoc init
    subparsers.add_parser('init')

    # bchoc verify
    subparsers.add_parser('verify')

    args = parser.parse_args()

    if args.command == 'add':
        ADD.add(args.case_id, args.item_id, args.creator, args.password)
        # ic(args.command)
        # ic(args.case_id)
        # ic(args.item_id)
        # ic(args.creator)
        # ic(args.password)

    if args.command == 'checkout':
        # ic(args.command)
        # ic(args.item_id)
        # ic(args.password)
        CHECKOUT.checkout(args.item_id, args.password)
        #sys.exit(1)

    if args.command == 'checkin':
        CHECKIN.checkin(args.item_id, args.password)
        # ic(args.command)
        # ic(args.item_id)
        # ic(args.password)
        # checkin_function()

    if args.command == 'show':
        if args.show_command == 'cases':
            sys.exit(1)
            # ic(args.show_command)
            # ic(args.password)
            # show_cases_function()
        if args.show_command == 'items':
            sys.exit(1)
            # ic(args.show_command)
            # ic(args.case_id)
            # ic(args.password)
            # show_items_function()
        if args.show_command == 'history': # Note: If optional args are not provided, they will be None
            sys.exit(1)
            # ic(args.show_command)
            # ic(args.case_id)
            # ic(args.item_id)
            # ic(args.num_entries)
            # ic(args.reverse)
            # ic(args.password)
            # show_history_function()
    
    if args.command == 'remove': # Note: If optional args are not provided, they will be None
        REMOVE.remove(args.item_id, args.password, args.reason)
        # ic(args.command)
        # ic(args.item_id)
        # ic(args.reason)
        # ic(args.password)
        # remove_function()

    if args.command == 'init':
        INIT.init()
        sys.exit(0)
        # ic(args.command)
        # init_function()

    if args.command == 'verify':
        sys.exit(1)
        # ic(args.command)
        # verify_function()


if __name__ == "__main__":
    blockchain_file_path = os.getenv('BCHOC_FILE_PATH')
    if blockchain_file_path:
        CONS.filePath = blockchain_file_path
    main()
