import boto

class EnvError(Exception):
    pass

class EC2Error(Exception):
    pass

class ElbConnection(object):
    def __init__(
        self,
        aws_key,
        aws_secret,
        debug = False
    ):
        self.debug = debug
        if aws_key and aws_secret:
            self.aws_key = aws_key
            self.aws_secret = aws_secret
        else:
            raise EnvError('EC2_ACCESS_KEY and EC2_SECRET_KEY environment variables are not set, or did not pass -k -s options at runtime.')

    def connect(self):
        '''
        just a basic EC2 api connection
        '''
        return boto.connect_elb(self.aws_key, self.aws_secret)

    def get_elb_list(self):
        '''
        gets a list of all ELBs attached to this aws account
        '''
        self.conn = self.connect()
        return self.conn.get_all_load_balancers()

    def does_elb_exist(self, elb_name):
        '''
        connects to aws api, and checks to see if there is an elb named elb_name
        '''
        self.conn = self.connect()
        data = self.conn.get_all_load_balancers(elb_name)
        if self.debug: print 'found elb: ' + str(data)
        if data:
            return True
        else:
            return False

    def _elb_instance_loop(self, elb_name, instance_name):
        '''
        connects to aws api, assumes that the elb exists, and then loops through
        the list of members in the elb looking for instance_name
        '''
        self.conn = self.connect()
        self.instance_list = self.conn.describe_instance_health(elb_name)
        if self.debug: print 'list of instances in %s: %s' % (elb_name, str(self.instance_list))
        for i in self.instance_list:
            if self.debug: print 'checking instance: ' + i.instance_id
            if i.instance_id == instance_name:
                if self.debug: print 'found instance in list: ' + i.instance_id
                return True
            else:
                self.instance_in_elb = False
        return self.instance_in_elb

    def is_instance_elb_member(self, elb_name, instance_name):
        '''
        checks to see if the elb name is valid, then runs the private method 
        to loop the list that is output from boto's describe_instance_health
        '''
        if self.does_elb_exist(elb_name):
            return self._elb_instance_loop(elb_name, instance_name)
        else:
            return False

    def add_instance_to_elb(self, elb_name, instance_name):
        '''
        checks to see if the elb exists, and if the instance is not already a
        member of the elb. Then registers the instance to the elb.
        '''
        if not self.does_elb_exist(elb_name):
            raise EC2Error('ELB does not exist: ' + elb_name)
        else:
            if self.is_instance_elb_member(elb_name, instance_name):
                raise EC2Error('Instance %s is already a member of %s' % (instance_name, elb_name))
            else:
                return self.conn.register_instances(elb_name, instance_name)

    def remove_instance_from_elb(self, elb_name, instance_name):
        '''
        checks to see if elb exists and if the instance is a member.
        Then it removes the instance from the elb.
        '''
        if not self.does_elb_exist(elb_name):
            raise EC2Error('ELB does not exist: ' + elb_name)
        else:
            if not self.is_instance_elb_member(elb_name, instance_name):
                raise EC2Error('Instance %s is not a member of %s' % (instance_name, elb_name))
            else:
                return self.conn.deregister_instances(elb_name, instance_name)


