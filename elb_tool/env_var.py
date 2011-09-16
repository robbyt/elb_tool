import os

class EnvError(Exception):
    pass

def get_var_value(var,msg=None):
    try:
        return os.environ[var]
    except KeyError:
        if msg:
            raise EnvError(msg)
        else:
            raise EnvError('Could not find env var for: ' + var )
        
