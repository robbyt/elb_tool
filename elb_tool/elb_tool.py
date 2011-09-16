#!/usr/bin/env python
import sys, argparse
import os

class UserInput(object):
    usage = "Please read --help"

    def __init__(self, args):
        '''
        sets up the user input system. When setting up this 
        class, pass sys.argv[1:] into the class, otherwise for testing
        pass in a list of simulated arguments
        '''
        
        # setup the parser
        self.parser = argparse.ArgumentParser(description='elb_tool')

        # prep some variables
        self.args = args
        self.elb_help = 'elb help goes here'
        self.instance_help = 'instance help goes here'

        #run the arg parser methods
        self._setup_args()

    def _setup_args(self):
        '''operands, or server/cluster to perform an operation on'''
        # elb_name
        self.parser.add_argument(
            "-e", "--elb",
            dest="elb_name",
            help=self.elb_help,
            #choices=
            required=True
        )

        self.parser.add_argument(
            "-i", "--instance",
            dest="instance_name",
            help=self.instance_help,
            #default=
            required=True
        )

        ## other options
        self.parser.add_argument("--debug", action="store_true", dest="debug", default=False)
        self.parser.add_argument("-n", "--noop", action="store_true", dest="noop")

    def _parse_args(self):
        return self.parser.parse_args(self.args)
    
    def get_args_as_dict(self):
        return vars(self._parse_args())

    def debug_enabled(self):
        res = self._parse_args()
        if res.debug:
            return True
        else:
            return False

if __name__ == '__main__':
    ui = UserInput(sys.argv[1:])
    ui.debug_enabled()
    if ui.debug_enabled():
        print ui.get_args_as_dict()
