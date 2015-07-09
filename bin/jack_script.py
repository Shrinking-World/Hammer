'''
Jack Script

Command interpreter for Jack Hammer scripting language.

Functional requirements:

 * Run from the Linux shell
 * Each line of stdin is a script command
 * Blank line or 'exit' ends to the program
 * Illegal command shows the help text
 * Jack Script has a self test 
 * Description is contained in the source code

Next steps:

'''


# Run the test for Jack Script
def jack_script_test():
    print ('jack_script_test()')


# Run the test for Jack Script
def jack_script_help(command):
    print ('Unknown command:  %s'%command)
    help_text = '''
        Jack Script Commands:
            test -- run the requested tests
    '''
    print (help_text)


# Read and do a single command
def read_and_exec(command):
    if not command or command=='exit':
        return False
    if command=='test':
        jack_script_test()
        return True
    jack_script_help(command)
    return True


# REPL for Jack Script
def jack_script_loop():
    print ('Jack Hammer Script Commander:')
    while read_and_exec(input(' ? ')):
        pass
    print ('Jack Script done')


# Run as a stand-alone script
if __name__=='__main__':
    jack_script_loop()
