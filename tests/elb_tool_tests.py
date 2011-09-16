from nose.tools import *
from elb_tool.elb_tool import *

def debug_test():
    ui = UserInput(['-e', 'elb', '-i', 'inst', '--debug'])
    assert_equal(ui.debug_enabled(), True)


