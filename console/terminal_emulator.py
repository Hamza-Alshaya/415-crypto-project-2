import sys
sys.path.append('./')



#terminal emulator function:
def terminal_emulator(name='myName'):
    import console.commands
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
        print('/h, /help, /?:\t\t\tdisplay help menu.')
        print('/toggle encryption, /t e:\tEnable or disable encryption')
        print('/toggle decryption, /t d:\tEnable or disable decryption')
        print('/info, /i:\t\t\tShow current config variables')
        print('/hash tamper:\t\t\tTamper with the hash sent to the other end')
        
        print('\n')
        return f'/'
    
    elif macro == console.commands.TOGGLE_ENCRYPTION_COMMAND:
        if (name == "Alice"):
            import console.alice_config
            console.alice_config.enable_encryption = not(console.alice_config.enable_encryption)
            print(f'Encrypting outgoing messages has been set to {console.alice_config.enable_encryption}.')
            return f'/'
        
        elif (name =='Bob'):
            import console.bob_config
            console.bob_config.enable_encryption = not(console.bob_config.enable_encryption)
            print(f'Encrypting outgoing messages has been set to {console.bob_config.enable_encryption}.')
            return f'/'
        
    elif macro == console.commands.TOGGLE_DECRYPTION_COMMAND:
        if (name == "Alice"):
            import console.alice_config
            console.alice_config.enable_decryption = not(console.alice_config.enable_decryption)
            print(f'Decrypting incoming messages has been set to {console.alice_config.enable_decryption}.')
            return f'/'
        
        elif (name =='Bob'):
            import console.bob_config
            console.bob_config.enable_decryption = not(console.bob_config.enable_decryption)
            print(f'Decrypting incoming messages has been set to {console.bob_config.enable_decryption}.')
            return f'/'
    
    elif macro == console.commands.SHOW_INFO_COMMAND:
        if (name == "Alice"):
            import console.alice_config
            print(f"Encrypting outgoing messages: {console.alice_config.enable_encryption}")
            print(f"Decrypting incoming messages: {console.alice_config.enable_decryption}")
            return f'/'
        
        elif (name =='Bob'):
            console.bob_config
            print(f"Encrypting outgoing messages: {console.bob_config.enable_encryption}")
            print(f"Decrypting incoming messages: {console.bob_config.enable_decryption}")
            return f'/'
    elif macro == console.commands.TAMPER_HASH_COMMAND:
        if (name == "Alice"):
            import console.alice_config
            console.alice_config.emulate_false_hash = not (console.alice_config.emulate_false_hash)
            print(f'Tampering with the sent hash has been set to {console.alice_config.emulate_false_hash}')
            
            return f'/'
        elif (name =='Bob'):
            import console.bob_config
            console.bob_config.emulate_false_hash = not (console.bob_config.emulate_false_hash)
            print(f'Tampering with the sent hash has been set to {console.bob_config.emulate_false_hash}')
            return f'/'

    elif macro == console.commands.PLAIN_TEXT:
        return input_string
    elif macro == console.commands.EMPTY_STRING:
        #We will send a space character to avoid errors with the encode() function
        return "/"
