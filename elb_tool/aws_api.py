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
        return boto.connect_elb(self.aws_key, self.aws_secret)

    def get_elb_list(self):
        self.conn = self.connect()
        return self.conn.get_all_load_balancers()

