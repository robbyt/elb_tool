from nose.tools import *
from elb_tool.aws_api import *
import os

def env_test_key():
    conn = ElbConnection()
    assert_equal(conn.aws_key, os.environ.get('EC2_ACCESS_KEY'))

def env_test_sec():
    conn = ElbConnection()
    assert_equal(conn.aws_secret, os.environ.get('EC2_SECRET_KEY'))

def env_test_empty_env():
    with assert_raises(EnvError):
        conn = ElbConnection('','')
    
