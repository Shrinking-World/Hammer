#!/usr/bin/env python

from os import system, listdir, environ
from os.path import join, exists
from sys import argv

from diff_tests import shell


def command_add(argv):
	'''	
	Create a new command.
	'''
	print("Add new command:"+argv[2])
	command = argv[2]
	path1 = join(environ['pb'],'%s.py' % command)
	path2 = join(environ['pb'],'prototype.py')
	command_content = open(path2).read().replace('prototype',command)
	#print('Content: %s.py \n %s' % (command,command_content))
	if exists(path1):
		print('File already exists: '+path1)
	else:
		with open(path1,'w') as f:
			f.write(command_content)
	#command_edit(argv)


def command_delete(argv):
	'''	
	Delete the command.
	'''
	print("Command:",argv[2])
	print(shell('rm bin/%s.py' % argv[2]))


def command_edit(argv):
	'''	
	Edit the content of a command.
	'''
	print("Command:",argv[2])
	print(shell('e bin/%s.py' % argv[2]))


def command_help():
	'''
	Show all the command commands and their usage.
	'''
	print('''
	usage: cmd command [args]

    command:

        add     [file] -- Add a new command
        delete  [file] -- Delete a command
        edit    [file] -- Edit the command
        list    [file] -- List all commands
        show    [file] -- Show a command
      
			''')


def command_list(argv):
	'''
	List the parts of the command source code.
	'''
	print("List the contents of this command")
	for d in ('bin',):
		print(d+':')
		print('    '+'\n    '.join(listdir(join(environ['p'],d))))


def command_show(argv):
	'''	
	Show the content of a command.
	'''
	path = join(environ['pb'],argv[2]+'.py')
	if not exists(path):
		print('Command not found: '+path)
	else:
		print("Command:",path)
		print(open(path).read())


def command_command(argv):
	'''
	Execute all of the command specific commands
	'''
	if len(argv)>1:

		if argv[1]=='add-test':
			command_add(argv)
			exit(0)

		elif argv[1]=='add':
			command_add(argv)
			command_edit(argv)
			exit(0)

		elif argv[1]=='delete':
			command_delete(argv)
			exit(0)

		elif argv[1]=='edit':
			command_edit(argv)
			exit(0)

		elif argv[1]=='list':
			command_list(argv)
			exit(0)

		elif argv[1]=='show':
			command_show(argv)
			exit(0)

		else:
			print('No command command found, '+argv[1])
		
	command_help()


'''
Create a script that can be run from the shell
'''
if __name__=='__main__':
	command_command(argv)