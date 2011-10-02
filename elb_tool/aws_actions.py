import sys
import aws_api

class AwsActions(object):
    def __init__(self, **kwargs):
        self.instance_name = kwargs['instance_name']
        self.elb_name = kwargs['elb_name']
        self.debug = kwargs['debug']
        self.noop = kwargs['noop']
        self.action = kwargs['action_name']
        self.aws_key = kwargs['aws_key']
        self.aws_secret = kwargs['aws_secret']
    
        self.ec2 = self.connect()
        
    def connect(self):
        try:
            return aws_api.ElbConnection(
                debug=self.debug,
                aws_key=self.aws_key,
                aws_secret=self.aws_secret
            )
        except aws_api.EnvError, e:
        # EnvError will be raised if we cannot find the connection key/secret
            print e
            sys.exit(1)

    def check(self):
        if not self.noop:
            try:
                self.is_member = self.ec2.is_instance_elb_member(self.elb_name, self.instance_name)
            except aws_api.EnvError, e:
                print e
        else:
            self.is_member = False

        if self.is_member:
            print "Yes, %s is a member of %s" % (self.instance_name, self.elb_name)
            sys.exit(0)

        elif not self.is_member:
            print "No, %s is not a member of %s, or is an invalid instance ID" % (self.instance_name, self.elb_name)
            sys.exit(1)


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

