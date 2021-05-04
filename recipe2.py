#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CODE DESCRIPTION HERE

Created on 2021-01-2021-01-05 13:59

@author: cook
"""
import argparse
import datetime
import logging
import random
import time

# =============================================================================
# Define variables
# =============================================================================
# define logger
logger = logging.basicConfig(filename='apero-log.txt', level=logging.INFO,
                             format='%(asctime)s | %(levelname)s | %(message)s')
# define sleep time
SLEEP_TIME = 5

# =============================================================================
# Define functions
# =============================================================================
def main(group_num=None, run_num=None):

    # set up arguments
    if group_num is None or run_num is None:
        # set up arguments
        parser = argparse.ArgumentParser(description='This is a mock recipe')
        parser.add_argument('group_num', nargs=1, type=int)
        parser.add_argument('run_num', nargs=1, type=int)
        # get arguments
        args = parser.parse_args()
        # print and log message
        margs = [args.group_num, args.run_num]
    else:
        margs = [group_num, run_num]

    msg = 'RECIPE2: Running group {0} run {1}'.format(*margs)
    print(msg)
    logging.info(msg)

    # add a random time component
    rtime = random.randint(-SLEEP_TIME//2, SLEEP_TIME//2)
    # sleep
    time.sleep(SLEEP_TIME + rtime)

    return msg


# =============================================================================
# Start of code
# =============================================================================
if __name__ == "__main__":
    _msg = main()

# =============================================================================
# End of code
# =============================================================================
