from nose.tools import *
from elb_tool.user_input import *

def debug_test():
    ui = UserInput(['-e', 'elb', '-i', 'inst', '--debug', '-a', 'check'])
    assert_equal(ui.debug_enabled(), True)

def debug_test2():
    ui = UserInput(['-e', 'elb', '-i', 'inst', '--debug', '-a', 'check'])
    data = ui.get_args_as_dict()
    return_dict = {'instance_name': 'inst', 'debug': True, 'elb_name': 'elb', 'noop': False, 'action_name': 'check'}
    assert_equal(data, return_dict)
    
def noop_test():
    ui = UserInput(['-e', 'elb', '-i', 'inst', '--debug', '--noop', '-a', 'check'])
    data = ui.get_args_as_dict()
    return_dict = {'instance_name': 'inst', 'debug': True, 'elb_name': 'elb', 'noop': True, 'action_name': 'check'}
    assert_equal(data, return_dict)
    
