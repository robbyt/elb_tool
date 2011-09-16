from nose.tools import *
import elb_tool.aws_api
import os

def env_test():
    conn = elb_tool.aws_api.ElbConnection()
    assert_equal(conn.aws_key, os.environ.get('EC2_ACCESS_KEY'))

def env_test2():
    conn = elb_tool.aws_api.ElbConnection()
    assert_equal(conn.aws_secret, os.environ.get('EC2_SECRET_KEY'))
    
