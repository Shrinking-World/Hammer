'''
Tests for prototype code
-------------------

Run all of the tests for the 'prototype' objects.  Output the test results.

'''

from os import listdir, environ, system
from os.path import join

from shell import shell, lines, limit_lines


def prototype_list_test():
    return shell('prototype list')


def prototype_path_test():
    return shell('prototype path') + '\n' + shell('prototype path xxx')


def prototype_show_test():
    return shell('prototype show prototype.py')
