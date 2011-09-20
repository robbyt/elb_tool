#!/usr/bin/env python
import sys, argparse
import aws_api
from user_input import *

class ElbTool(object):
    def __init__(self, **kwargs):
        self.instance_name = kwargs['instance_name']
        self.elb_name = kwargs['elb_name']
        self.debug = kwargs['debug']
        self.noop = kwargs['noop']
        self.action = kwargs['action_name']
        self.aws_key = kwargs['aws_key']
        self.aws_secret = kwargs['aws_secret']
        
        self.ec2 = aws_api.ElbConnection(
            debug=self.debug,
            aws_key=self.aws_key,
            aws_secret=self.aws_secret
        )

    def check(self):
        if not self.noop:
            if self.ec2.is_instance_elb_member(self.elb_name, self.instance_name):
                print "Yes, %s is a member of %s" % (self.instance_name, self.elb_name)
                sys.exit(0)
            else:
                print "No, %s is not a member of %s" % (self.instance_name, self.elb_name)
                sys.exit(1)
        else:
            print 'Check not run, because we are in noop mode'

    def add(self):
        try:
            if not self.noop:
                self.ec2.add_instance_to_elb(self.elb_name, self.instance_name)
            print 'Added %s to %s' % (self.instance_name, self.elb_name)
            sys.exit(0)
        except aws_api.EC2Error, e:
            print e
            sys.exit(1)
            
    def remove(self):
        try:
            if not self.noop:
                self.ec2.remove_instance_from_elb(self.elb_name, self.instance_name)
            print 'Removed %s from %s' % (self.instance_name, self.elb_name)
            sys.exit(0)
        except aws_api.EC2Error, e:
            print e
            sys.exit(1)

    def run(self):
        if self.action == 'check':
            self.check()
        elif self.action == 'add':
            self.add()
        elif self.action == 'remove':
            self.remove()
        else:
            print 'Error: can not find your action in action_name'
            sys.exit(1)

if __name__ == '__main__':
    # parse the args
    ui = UserInput(sys.argv[1:])

    # collect the parsed args into a dict
    data = ui.get_args_as_dict()

    # throw that dict at the ElbTool to do stuff with the AWS api
    action = ElbTool(**data)
    action.run()
