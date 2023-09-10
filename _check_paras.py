import sys
import re

########################################
# Check the number of arguments passed to the script
########################################

PARAMETER_NUM = 2
PARA_REGEX = ['^ADD=(\d{1})$', '^PATH=([0-9a-zA-Z_-]{1,10}\.py)$']
PARA_EXPLAIN = '\nYou can use \n"python3 {current script name}.py ADD=1 PATH=12345.py"\nto run this script.'

def checkArg():
    try:
        # Get all the arguments passed to the script
        args = sys.argv

        # Get the number of arguments
        arg_num = len(args) - 1

        # Check if the number of arguments is equal to PARAMETER_NUM
        if arg_num != PARAMETER_NUM:
            raise ValueError(f"Error 1: Expected {PARAMETER_NUM} parameters, but got {arg_num}")

        # Extract the parameters from the arguments
        params = {}
        for i, arg in enumerate(args[1:]):
            params[i] = arg

        return params
    except Exception as e:
        raise ValueError(f"Error 2:{e}")

def checkArgRegex(param, regex):
    match = re.match(regex, param)
    if match:
        return match.group(1)
    else:
        raise ValueError(f"Error 0: Invalid parameter format: {param}")

try:
    params = checkArg()
    para_regex_ = [checkArgRegex(params[i], PARA_REGEX[i]) for i in range(PARAMETER_NUM)]

    # Print the parameter list
    for i, para in enumerate(para_regex_):
        print(f"para {i}: [{para}]")

    # Validate parameter values
    ADD = int(para_regex_[0])
    if ADD not in [0, 1]:
        raise ValueError("Error 3: ADD parameter must be 0 or 1")
except ValueError as e:
    print(f"Error 4: {e}")
    print(f"{PARA_EXPLAIN}")
    exit(1)
    
########################################
# End of argument checking section
########################################
