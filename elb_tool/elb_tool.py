#!/usr/bin/env python
import sys, argparse, os
from user_input import *

if __name__ == '__main__':
    ui = UserInput(sys.argv[1:])
    data = ui.get_args_as_dict()
