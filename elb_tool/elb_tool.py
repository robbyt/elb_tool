#!/usr/bin/env python
import sys, argparse
from user_input import *
from aws_api import *

class ElbTool(object):
    def __init__(self, **kwargs):
        self.instance_name = kwargs['instance_name']
        self.elb_name = kwargs['elb_name']
        self.debug = kwargs['debug']
        self.noop = kwargs['noop']

if __name__ == '__main__':
    # parse the args
    ui = UserInput(sys.argv[1:])

    # collect the parsed args into a dict
    data = ui.get_args_as_dict()

    # throw that dict at the ElbTool to do stuff with the AWS api
    action = ElbTool(data)
