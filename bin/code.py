#!/usr/bin/env python

from glob import glob
from os import system, listdir, environ, chdir
from os.path import join, isdir
from sys import argv

from code_test import code_checker


def calculate_complexity(filename):
	text = open(join(environ['p'],filename)).read()
	lines = text.split('\n')
	num_imports = len([i for i in lines if 'import' in i])
	import_cost = 10  # Equal to 10 lines of code
	num_lines = len(lines)
	coupling_cost = 1.2 # Exponential penalty of size
	complexity = (num_lines + num_imports * import_cost) ** coupling_cost
	return (num_lines,num_imports,complexity)


def code_complexity(files=None):
	'''Measure the code complexity'''
	print ('code_complexity:',files)
	if not files:
		files = code_list().split('\n')
	python_files = [f for f in files if f.endswith('.py')]
	total = (0,0,0)

	print('File                              Lines  Imports Complexity')

	for f in sorted(python_files):
		lines,imports,complexity = calculate_complexity(f)
		total = (total[0]+lines, total[1]+imports, total[2]+complexity)
		print('%-30s' % f, '%8d' % lines, '%8d' % imports, '%8d' % complexity)

	print('%-30s %8d %8d %8d' % ('Total',total[0], total[1], total[2]))


def code_help():
	'''Show all the code codes and their usage.'''
	print('''
	usage: cmd code [args]

    code:
    	complexity     -- Calculate the complexity of the source code
        list    [file] -- List all codes
        show    [file] -- Show a code
        test           -- Self test
      
			''')


def code_list(files=None):
	'''List the files of source code.'''
	results = []
	if not files:
		files = ['bin']
	for d in files:
		chdir(environ['p'])
		files = [f for f in glob(d+'/*') if not isdir(f)]
		files = [f for f in files if not f.endswith('.pyc')]
		results.append('\n'.join(files))
	return '\n'.join(results)


def code_show(files):
	'''Show the content of a code.'''
	print("code:",files)
	if not files:
		files = code_list().split('\n')
	for f in files:
		system('cat %s' % f)


def code_command(argv):
	'''Execute all of the code specific codes'''
	if len(argv)>1:

		if argv[1]=='complexity':
			code_complexity()

		elif argv[1]=='list':
			print(code_list())

		elif argv[1]=='show':
			code_show(argv[2:])

		elif argv[1]=='test':
			code_checker()

		else:
			print('No code command found, '+argv[1])
			code_help()
	else:
		print('No arguments given')
		code_help()


'''
Create a script that can be run from the shell
'''
if __name__=='__main__':
	code_command(argv)