import sys
sys.path.append('./')
import console.commands

#terminal emulator function:
def terminal_emulator(name='myName'):
    #read input and pass it to read command method to determine the type of command
    input_string = input(f'{name}: ')
    macro = console.commands.read_command(input_string)
    
    if macro == console.commands.UNKNOWN_COMMAND:
        print("Error: Unknown command. See /? for list of commands.")
        return f'/'
    
    elif macro == console.commands.EXIT_COMMAND:
        return f'/{console.commands.EXIT_COMMAND}'
    
    elif macro == console.commands.HELP_COMMAND:
        print('/c, /close, /q, /quit:\t\tQuit the program.')
        print('/h, /help, /?:\t\tdisplay help menu.')
        return f'/'
        
    elif macro == console.commands.PLAIN_TEXT:
        return input_string
    elif macro == console.commands.EMPTY_STRING:
        #We will send a space character to avoid errors with the encode() function
        return "/"
