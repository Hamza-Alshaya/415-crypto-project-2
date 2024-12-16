#MACROS that are used to define the type of command 
EMPTY_STRING = -2
UNKNOWN_COMMAND = -1
PLAIN_TEXT = 0
EXIT_COMMAND = 1
HELP_COMMAND = 2
TOGGLE_DECRYPTION_COMMAND = 3
TOGGLE_ENCRYPTION_COMMAND = 4

import sys
sys.path.append('./')

#return the macro of the adequate command
def define_command(input):
    if (input == '/q' or input == '/quit' or input == '/c' or input == '/close'):
        return EXIT_COMMAND
    elif (input == '/h' or input == '/help' or input == '/?'):
        return HELP_COMMAND
    elif (input == "/toggle encryption" or input == "/t e"):
        return TOGGLE_ENCRYPTION_COMMAND
    elif (input == "/toggle decryption" or input == "/t d"):
        return TOGGLE_DECRYPTION_COMMAND
    else:
        return UNKNOWN_COMMAND

#wrapper function to define command; checks if it's a valid command or a simple string
def read_command(input):
    #empty string avoidance
    if (len(input) > 0 ):
        if (input[0] == '/'):    #it's a command
            return define_command(input)
        else:
            return PLAIN_TEXT
    else:
        return EMPTY_STRING