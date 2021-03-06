#!/usr/bin/env python

from os import environ, listdir, remove, system,  walk
from os.path import dirname, exists, isdir, isfile, join
from random import choice
from subprocess import Popen,PIPE
from sys import argv

# Read in shell variables
ON_INTERNET = environ['ON_INTERNET']=="True"


def on_internet():
    if ON_INTERNET:
        return True
    else:
        print ('No internet connection')
 

def select_lines(text, first, last):
    return '\n'.join(text.split('\n')[first:last])


def delete_file(path):
    '''Delete the notes.'''
    #print("Delete file: "+path)
    if exists(path):
        remove(path)
    else:
        print('File does not exist: '+path)


def add_file(path,topic):
    '''Create a new notes.'''
    if topic:
        path = join(path,topic)
        #print("New file:"+path)
        dir = dirname(path)
        if not exists(dir):
            print('creating directory, '+dir)
            mkdir (dir)
        if not exists(path):
            with open(path,'w') as f:
                f.write('# '+topic)
        else:
            print('File already exists: '+path)
        return path
    else:
        print('Must give a file name')


def edit_file(path):
    '''Edit the content of a file.'''
    if path:
        print("Edit task:",path)
        if exists(path):
            system('e '+path)
        else:
            print('File does not exist: '+path)
    else:
        print('No topic specified')


def enumerate_files(base, topic=None):
    '''Generator to produce a list of all files in a tree'''
    path = base
    if topic:
        path = join(path,topic)
    for root, dirnames, filenames in walk(path):
        if not '.git' in root: 
            for filename in filenames:
                yield join(root, filename).replace(base+'/','')


def print_file_list(base, topic=None):
    '''List the files of a subdirectory.'''
    print ('\n'.join(sorted(enumerate_files(base,topic))))


def print_banner(name):
    '''Show a banner for this file in the output'''
    print('\n%s\n%s%s\n%s\n' % ('-'*80, ' '*30, name,'-'*80))


def print_file(path):
    '''Print text from a file'''
    print (read_file(path))


def show_files(root_dir, topic=None):
    ''' Show the content of one file or directory'''
    selection = root_dir
    if topic:
        selection = join(selection,topic)
    if isdir(selection):
        for f in enumerate_files(root_dir, topic):
            path = join(root_dir,f)
            if isfile(path):
                print_banner (f)
                print_file(path)
    elif isfile(selection):
        print_file(selection)


def read_file(path):
    '''Read text from a file'''
    if exists(path):
        return open(path).read().decode('ascii','ignore')
    else:
        return ''
        

def write_file(path,text):
    '''Write text to a file'''
    return open(path, 'w').write(text)


def limit_lines(shell_command, min=None, max=None):
    '''Limit the lines to a certain number or echo all the output'''
    text = shell (shell_command)
    violation = lines(text,min,max)
    if violation:
        text = text.split('\n')
        text = '\n'.join([line[:60] for line in text])
        #return violation+'\n'+text
        return violation
    return ''


def lines(text, min=None, max=None):
    '''Guarantee that there are the correct number of lines in the text.'''
    num_lines_output = len(text.split('\n'))
    if min and num_lines_output<min:
        return('Min count lines: actual=%d, min=%d' % (num_lines_output, min))
    if max and num_lines_output>max:
        return('Max count lines: actual=%d, max=%d' % (num_lines_output, max))


def shell(command):
    '''   Execute a shell command and return its output   '''
    output = Popen(command.split(' '), stdout=PIPE).stdout
    return output.read().decode(encoding='UTF-8')


def differences(answer,correct):
    '''   Calculate the diff of two strings   '''
    if answer!=correct:
        t1 = '/tmp/diff1'
        t2 = '/tmp/diff2'
        with open(t1,'wt') as file1:
            #print (answer)
            file1.write(str(answer)+'\n')
        with open(t2,'wt') as file2:
            file2.write(str(correct)+'\n')
        diffs = shell('diff %s %s' %(t1, t2))
        if diffs:
            #print('Differences detected:     < actual     > expected')
            #print (diffs)
            return diffs


def shell_add(topic):
    '''Create a new shell.'''
    path = shell_add_test(topic)
    system('e '+path)


def shell_add_test(topic):
    '''Create a new shell.'''
    if topic:
        path = shell_path(topic)
        print("New shell:"+path)
        if exists(path):
            print('File already exists: '+path)
            return path
        with open(path,'w') as f:
            f.write('# shell: '+topic)
        return path
    else:
        print('Must add a topic')


def shell_delete(topic):
    '''Delete the shell.'''
    path = shell_path(topic)
    print("Delete shell: "+path)
    if exists(path):
        remove(path)
    else:
        print('File does not exist: '+path)


def shell_edit(topic):
    '''Edit the content of a shell.'''
    if not topic:
        print('No topic specified')
        return
    path = shell_path(topic)
    print("Edit shell:",path)
    if exists(path):
        system('e '+path)
    else:
        print('File does not exist: '+path)


def shell_help():
    '''Show all the shell shells and their usage.'''
    print('''
    usage: cmd shell [args]

    shell:

        add     [file] -- Add a new shell
        delete  [file] -- Delete a shell
        edit    [file] -- Edit the shell
        list    [file] -- List all shells
        path    [file] -- Lookup the path for the file
        show    [file] -- Show a shell
      
            ''')


def shell_enumerate():
    '''Generator to produce a list of all topics'''
    root_dir = shell_path()
    for root, dirnames, filenames in walk(root_dir):
        for filename in filenames:
            yield join(root, filename).replace(root_dir+'/','')


def shell_list(root_dir,topic=None):
    '''List the parts of the shell source code.'''
    print("List the contents of this shell")
    for root, dirnames, filenames in walk(root_dir):
        for filename in filenames:
            if topic:
                if not topic == filename:
                    continue
            print(join(root, filename).replace(root_dir+'/',''))


def shell_path(topic=None):
    if topic:
        return join(environ['pb'],topic)
    else:
        return environ['pb']


def shell_pick(topic):
    '''Select a topic to edit'''
    system('e '+shell_path(choice(list(shell_enumerate()))))


def shell_show(topic):
    '''Show the content of a shell.'''
    if topic:
        path = shell_path(topic)
        print("Show shell: "+path)
        if exists(path):
            print(open(path).read())
            return
        print('File does not exists: '+path)
    else:
        print('No topic listed')


def get_topic(argv):
    if len(argv)>2:
        return argv[2]
    

def shell_command(argv):
    '''Execute all of the shell specific shells'''
    if len(argv)>1:

        if argv[1]=='add':
            shell_add(get_topic(argv))

        elif argv[1]=='add_test':
            shell_add_test(get_topic(argv))

        elif argv[1]=='delete':
            shell_delete(get_topic(argv))

        elif argv[1]=='edit':
            shell_edit(get_topic(argv))

        elif argv[1]=='list':
            shell_list(shell_path(), get_topic(argv))

        elif argv[1]=='path':
            print(shell_path(get_topic(argv)))

        elif argv[1]=='pick':
            shell_pick(get_topic(argv))

        elif argv[1]=='show':
            shell_show(get_topic(argv))

        else:
            print('No shell command found, '+argv[1])
            shell_help()
    else:
        print('No arguments given')
        shell_help()


'''
Create a script that can be run from the shell
'''
if __name__=='__main__':
    shell_command(argv)

