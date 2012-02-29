import boto
import boto.ec2.elb
from boto.utils import get_instance_metadata
import timeout

DEFAULT_REGION = 'us-east-1'

class EnvError(Exception):
    pass

class EC2Error(Exception):
    pass

class ElbConnection(object):
    def __init__(
        self,
        aws_key,
        aws_secret,
        region,
        debug = False
    ):
        self.debug = debug

        # lookup region name, this is alittle weird because the 
        # get_instance_metadata() does not timeout on it's own.
        try:
            self.region = self._lookup_region_name(region)
        except timeout.TimeoutError:
            # if we timed out on the connection to the api, just default 
            # to DEFAULT_REGION instead. You must not be running this tool
            # from an EC2 machine?
            self.region = DEFAULT_REGION

        if aws_key and aws_secret:
            self.aws_key = aws_key
            self.aws_secret = aws_secret
        else:
            raise EnvError('EC2_ACCESS_KEY and EC2_SECRET_KEY environment variables are not set, or did not pass -k -s options at runtime.')

    @timeout.timeout(5)
    def _lookup_region_name(self, region_input):
        """Look up the az name from checking the local instance metadata, 
        """
        if region_input is None:
            # we didn't set a region from the user input, so let's look it up
            az = get_instance_metadata()['placement']['availability-zone']
            return az[:-1]
        else:
            # we set a region from the input, so let's just return that
            return region_input

    def connect(self):
        '''
        just a basic EC2 api connection
        '''
#        return boto.connect_elb(self.aws_key, self.aws_secret)
        return boto.ec2.elb.connect_to_region(region_name=self.region,
                                              aws_access_key_id=self.aws_key,
                                              aws_secret_access_key=self.aws_secret)

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
        if self.debug: print 'could not find instance: ' + i.instance_id
        return False

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


