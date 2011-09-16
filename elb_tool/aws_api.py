import boto

class ElbConnection(object):
    def __init__(self, aws_key, aws_secret):
       self.aws_key = aws_key
       self.aws_secret = aws_secret

    def connect(self):
        return boto.connect_elb(self.aws_key, self.aws_secret)

    def get_elb_list(self):
        self.conn = self.connect()
        return self.conn.get_all_load_balancers()


