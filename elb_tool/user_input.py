#!/usr/bin/env python
import sys, argparse, os

class UserInput(object):
    usage = "Please read --help"

    def __init__(self, args):
        '''
        sets up the user input system. When setting up this 
        class, pass sys.argv[1:] into the class, otherwise for testing
        pass in a dict of simulated arguments
        '''
        
        # setup the parser
        self.parser = argparse.ArgumentParser(description='elb_tool')

        # prep some variables
        self.args = args
        self.htext = {
            'elb':'The ELB name. You must create this ELB somewhere else.',
            'instance':'EC2 instance ID',
            'action':'check/add/remove',
            'noop':'Will not actually interact with the AWS API, for testing',
            'key':'Your EC2 Access Key - can also be set via envar EC2_ACCESS_KEY',
            'secret':'Your EC2 Secret Key - can also be set via envar EC2_SECRET_KEY'
        }

        #run the arg parser methods
        self._setup_args()

    def _setup_args(self):
        '''operands, or server/cluster to perform an operation on'''
        # elb_name
        self.parser.add_argument(
            "-e", "--elb",
            dest="elb_name",
            help=self.htext['elb'],
            #choices=
            required=True
        )

        # instance name
        self.parser.add_argument(
            "-i", "--instance",
            dest="instance_name",
            help=self.htext['instance'],
            #default=
            required=True
        )

        self.parser.add_argument(
            "-k", "--key",
            dest="aws_key",
            help=self.htext['key'],
            default=os.environ.get('EC2_ACCESS_KEY')
        )

        self.parser.add_argument(
            "-s", "--secret",
            dest="aws_secret",
            help=self.htext['secret'],
            default=os.environ.get('EC2_SECRET_KEY')
        )

        # action
        self.parser.add_argument(
            "-a", "--action",
            dest="action_name",
            help=self.htext['action'],
            choices=['check', 'add', 'remove'],
            required=True
        )

        ## other options
        self.parser.add_argument("--debug", action="store_true", dest="debug", default=False)
        self.parser.add_argument("-n", "--noop", action="store_true", dest="noop", default=False, help=self.htext['noop'])

    def _parse_args(self):
        return self.parser.parse_args(self.args)
    
    def get_args_as_dict(self):
        d = vars(self._parse_args())
        if self.debug_enabled(): print 'parsed args in dict: ' + str(d)
        return d

    def debug_enabled(self):
        res = self._parse_args()
        return res.debug

    def noop_enabled(self):
        res = self._parse_args()
        return res.noop

