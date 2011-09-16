import boto, os

class EnvError(Exception):
    pass

class ElbConnection(object):
    def __init__(
        self,
        aws_key = os.environ.get('EC2_ACCESS_KEY'),
        aws_secret = os.environ.get('EC2_SECRET_KEY')
    ):
        if aws_key and aws_secret:
            self.aws_key = aws_key
            self.aws_secret = aws_secret
        else:
            raise EnvError('EC2_ACCESS_KEY and EC2_SECRET_KEY environment variables are not set.')

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
        for i in self.conn.describe_instance_health(elb_name):
            if i.instance_id == instance_name:
                return True
            else:
                return False

    def is_instance_elb_member(self, elb_name, instance_name):
    '''
    checks to see if the elb name is valid, then runs the private method 
    to loop the list that is output from boto's describe_instance_health
    '''
        if does_elb_exist(elb_name):
            return _elb_instance_loop(elb_name, instance_name)


