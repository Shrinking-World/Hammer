#!/usr/bin/env python

from datetime import datetime
from glob import glob
from os import system, listdir, environ, mkdir, getcwd, chdir
from os.path import join, exists
from subprocess import Popen,PIPE
from sys import argv

from code import find_functions
from shell import shell
from store import save, recall, expire, expiration, save_key, recall_key
from store import is_cached, clear_cache


def tst_add(command):
    '''Create a new test.'''
    print("Add new test:"+command)
    script_path = join(environ['pb'],'%s_test.py' % command)
    template_path = join(environ['pb'],'prototype_test.py')
    command_content = open(template_path).read().replace('prototype',command)
    if exists(script_path):
        print('File already exists: '+script_path)
    else:
        with open(script_path,'w') as f:
            f.write(command_content)


def tst_approve_results(testcases=None):
    '''Approve the test results'''
    if testcases:
        for name in testcases:
            answer = recall_key(name+'.out')
            if answer:
                save_key('%s.correct' % name, answer)
            else:
                print('No test script output: '+name)
                save_key('%s.correct' % name, 'No test script output')
    else:
        for name in tst_cases():
            print('TL'+name)
            tst_approve_results([name])



def test_case_name(function):
    '''Convert function name to test case name'''
    return function.replace('_test','').replace('_','-')


def tst_cases():
    '''Enumerate all of the test cases'''
    return [test_case_name(c) for c in tst_functions()]


def tst_command(argv):
    '''Execute the appropriate test command'''
    if len(argv)>1:
        cmd = argv[1]

        if 'like'==cmd:
            tst_approve_results(argv[2:])
            
        elif 'functions'==cmd:
            print('\n'.join(tst_functions(argv[2:])))

        elif 'status'==cmd:
            tst_show_status()

        elif 'results'==cmd:
            print('Test differences: all tests')
            tst_results()      

        elif 'names'==cmd:
            print('\n'.join(tst_modules()))

        elif 'list'==cmd:
            tst_show_cases()
    
        elif 'modules'==cmd:
            print('\n'.join(tst_modules()))

        elif 'test'==cmd:
            tst_execute_module('tst_test.py')

        elif 'help'==cmd:
            tst_help()

        else:
            print('no test found: '+cmd)
            tst_help()

    if len(argv)==3:
        cmd = argv[1]
        t = argv[2]

        if 'add'==cmd:
            tst_add(t)

        elif 'edit'==cmd:
            tst_edit(t)

        elif 'execute'==cmd:
            tst_execute_module(t+'_test.py')

        elif 'output'==cmd:
            tst_show_output(t)

        elif 'correct'==cmd:
            tst_show_expected(t)

        elif 'results'==cmd:
            print('Show results: %s' % t)
            tst_show_diff(t)

        else:
            print('bad command: '+cmd)


def tst_diff(name):
    '''Find the differences'''
    from shell import differences
    answer = recall_key ('%s.out' % name)
    correct = recall_key('%s.correct' % name)
    if answer!=correct:
        return differences(answer,correct)
 
def tst_edit(command):
    '''Edit the content of a test.'''
    print(shell('e bin/%s_test.py' % command))


def tst_help():
    '''   Show the details of the 'tst' command   '''
    print('''
    usage: tst [command] [testname]

    examples:
        tst                 # runs all the tests
        tst results         # display the differences from expected
        tst name            # runs a single test
        tst like name       # set the correct results
        tst output name     # show the output results
        tst correct name    # show the correct results
      
    subcommands of tst:

    No args
        accept     # Accept every answer
        list       # List the tests to run
        status     # Show the failing tests
        results    # Show the unexpected results
        functions  # List the test functions for all modules
        modules    # List all test modules

    One test arg
        output     # Show the output
        correct    # Show the correct output
        results    # Show the unexpected results

    Shortcut commands
        tlike      # tst like
        tres       # tst results
        tstatus    # tst status
        tout       # tst output
        tcorrect   # tst correct
        tst        # systest
        nose       # nosetests

            ''')


def tst_execute_all():
    '''Execute all of the test functions for module'''
    print('execute all')
    from code import find_functions
    for m in tst_modules():
        tst_execute_module(m)
    tst_show_status()


def tst_execute_module(module):
    '''Execute all of the test functions for module'''
    print('\n'+module)
    for t in tst_functions([module]):
        tst_execute_test_case(module,t)


def tst_execute_test_case(module, function):
    '''Run the selected test and process results'''
    import_name = module.replace('.py','')
    testcase = test_case_name(function)
    tst_run_case(testcase, import_name, function)


def tst_execute_timed_test(testcase, import_name, function):
    '''Execute the test and cache the results for an appropriate time'''
    start = datetime.now()
    exec("import "+import_name)
    exec("answer = %s.%s()" % (import_name,function))
    end   = datetime.now()

    t     = end-start
    seconds = "%d.%1d seconds"%(t.seconds, t.microseconds/100000)
    duration = 10+t.seconds*100
    print('    %-20s  ... %s '%(testcase,seconds))
    
    save_key('%s.out' % testcase, answer, duration)
    return answer


def tst_functions(module=None):
    '''Enumerate all of the test command functions'''
    if module:
        path = join(environ['pb'], module[0])
        return [f for f in find_functions(path) if f.endswith('_test')]
    else:
        result = []
        for module in tst_modules():           
            path = join(environ['pb'],module)
            result += [f for f in find_functions(path) if f.endswith('_test')]
        return result
           
   
def tst_modules():
    '''Enumerate all of the test command modules'''
    modules = [c for c in listdir(environ['pb']) if c.endswith('_test.py')]
    return sorted(modules)


def tst_results():
    cases = [test_case_name(c) for c in tst_functions()]
    for t in cases:
        if tst_diff(t):
            tst_show_diff(t)


def tst_run_case(testcase, import_name, function):
    '''   Run the test and check the results   '''
    cache = is_cached('%s.out' % testcase )
    if cache and not tst_diff(testcase):
        print("    cached results %-20s  ... %d seconds" % (testcase,cache))
        answer = recall_key(testcase+'.out')
    else:
        answer = tst_execute_timed_test(testcase, import_name, function)
    correct = recall_key(testcase+'.correct')
    if not correct:
        save_key('%s.correct' % testcase, answer)
    tst_show_diff(testcase)


def tst_show_cases():
    '''Enumerate all of the test command functions'''
    from code import find_functions
    for m in tst_modules():
        print('\n'+m)
        path = join(environ['pb'],m)
        for f in find_functions(path):
            if f.endswith('_test'):
                print('    '+test_case_name(f))


def tst_show_diff(name):
    '''Show the results for one test case'''
    answer = recall_key ('%s.out' % name)
    correct = recall_key('%s.correct' % name)
    d = tst_diff(name)
    if d:
        print('---------------------------------------------------------')
        print('                      '+name)
        print('---------------------------------------------------------')
        print(d)


def tst_show_expected(name):
    '''Lookup the expected correct result for this test'''
    print('Expected correct output from %s\n-----------------' % name)
    print(recall_key(name+'.correct'))


def tst_show_output(name):
    '''Show the output text for the last test run'''
    print('Output from %s\n-----------------' % name)
    print(recall_key(name+'.out'))


def tst_show_status():
    '''Display the tests that failed'''
    failures = ['    %-20s FAIL' % name for name in tst_cases() if tst_diff(name)]
    print('\n\nTest Status: %d tests failed' % len(failures))
    print('  '+'\n  '.join(failures))


# Create a script that can be run from the tst
if __name__=='__main__':

    chdir(environ['p'])
    if len(argv)==1:
        tst_execute_all()
    else:
        tst_command(argv)
