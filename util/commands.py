EMPTY_STRING = -2
UNKNOWN_COMMAND = -1
PLAIN_TEXT = 0
EXIT_COMMAND = 1
HELP_COMMAND = 2

def define_command(input):
    if (input == '/q' or input == '/quit' or input == '/c' or input == '/close'):
        return EXIT_COMMAND
    elif (input == '/h' or input == '/help' or input == '/?'):
        return HELP_COMMAND
    
    else:
        return UNKNOWN_COMMAND


def read_command(input):
    #empty string avoidance
    if (len(input) > 0 ):
        if (input[0] == '/'):    #it's a command
            return define_command(input)
        else:
            return PLAIN_TEXT
    else:
        return EMPTY_STRING