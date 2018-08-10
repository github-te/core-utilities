#!/usr/bin/env python3

import glob
import os
import sys

from .outputs import stdout, stderr


def cat(filenames=[]):
    '''Reads files in command-line order, printing them to stdout.

    A dash ('-') as a filename treats stdin as a file, printing it line-by-line
    until it encounters ^C.

    For a UNIX domain socket, cat connects to it and reads until EOF.
    '''

    if len(filenames) == 0:
        filenames = ['-', ]

    brokenpipe = False
    for filename in expand(filenames):
        try:
            for line in lines(filename):
                if line is None:
                    stdout('\n')
                else:
                    stdout(line)
        except KeyboardInterrupt:  # ^C always ends the program
            stdout('\n')
            sys.exit(0)
        except BrokenPipeError:  # piping to `head` breaks pipes
            brokenpipe = True
        except IsADirectoryError:
            stderr(f'ERROR: {filename} is a directory.\n')
        except PermissionError:
            stderr(f'ERROR: no permission to open {filename}.\n')

    if brokenpipe:
        sys.stderr.close()
    sys.exit(0)


def chgrp(group, files, **options):
    '''The chgrp utility sets the group ID of the file named by each file
    operand to the group ID specified by the group operand. It does not
    follow symbolic links.
    '''


def lines(filename):
    '''Yields lines of file or stdin until EOF or an exception occurs.'''
    if filename == '-':
        for line in sys.stdin:
            yield line
    else:
        for line in open(filename, 'rb'):
            yield line.decode('utf-8', errors='replace')


def expand(fileglobs):
    for fileglob in fileglobs:
        if fileglob == '-':
            yield fileglob
        else:
            processed = os.path.expandvars(fileglob)
            processed = os.path.expanduser(processed)
            filecount = 0
            for filename in glob.glob(processed):
                filecount += 1
                yield filename
            if filecount == 0:
                stderr(f'{fileglob}: no such file or directory\n')
