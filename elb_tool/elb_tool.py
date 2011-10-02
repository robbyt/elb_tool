#!/usr/bin/env python
import sys
from user_input import UserInput
from aws_actions import AwsActions 

if __name__ == '__main__':
    # parse the args
    ui = UserInput(sys.argv[1:])

    # collect the parsed args into a dict
    data = ui.get_args_as_dict()

    # throw that dict at the ElbTool to do stuff with the AWS api
    action = AwsActions(**data)
    action.run()
