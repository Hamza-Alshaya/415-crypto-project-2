import util.commands

#terminal emulator function:
def terminal_emulator():
    #read input and pass it to read command method to determine the type of command
    input_string = input()
    macro = util.commands.read_command(input_string)
    
    if macro == util.commands.UNKNOWN_COMMAND:
        print("Error: Unknown command. See /? for list of commands.")
        return f'/'
    
    elif macro == util.commands.EXIT_COMMAND:
        return f'/{util.commands.EXIT_COMMAND}'
    
    elif macro == util.commands.HELP_COMMAND:
        print('/c, /close, /q, /quit:\t\tQuit the program.')
        print('/h, /help, /?:\t\tdisplay help menu.')
        return f'/'
        
    elif macro == util.commands.PLAIN_TEXT:
        return input_string
    elif macro == util.commands.EMPTY_STRING:
        #We will send a space character to avoid errors with the encode() function
        return " "
