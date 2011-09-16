from nose.tools import *
from elb_tool.elb_tool import *

def debug_test():
    ui = UserInput(['-e', 'elb', '-i', 'inst', '--debug'])
    assert_equal(ui.debug_enabled(), True)

def debug_test2():
    ui = UserInput(['-e', 'elb', '-i', 'inst', '--debug'])
    data = ui.get_args_as_dict()
    return_dict = {'instance_name': 'inst', 'debug': True, 'elb_name': 'elb', 'noop': False}
    assert_equal(data, return_dict)
    

