#!/usr/bin/env python
import sys, argparse
from user_input import *
from aws_api import *

if __name__ == '__main__':
    ui = UserInput(sys.argv[1:])
    data = ui.get_args_as_dict()
