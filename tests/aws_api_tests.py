from nose.tools import *
from elb_tool.aws_api import *
import os

def env_test():
    conn = ElbConnection()
    assert_equal(conn.aws_key, os.environ.get('EC2_ACCESS_KEY'))

def env_test2():
    conn = ElbConnection()
    assert_equal(conn.aws_secret, os.environ.get('EC2_SECRET_KEY'))

def env_test3():
    with assert_raises(EnvError):
        conn = ElbConnection('','')
    
