#!/usr/bin/env python
import aws_api, aws_actions, user_input


if __name__ == '__main__':
    # parse the args
    ui = user_input.UserInput(sys.argv[1:])

    # collect the parsed args into a dict
    data = ui.get_args_as_dict()

    # throw that dict at the ElbTool to do stuff with the AWS api
    action = aws_actions.AwsActions(**data)
    action.run()
