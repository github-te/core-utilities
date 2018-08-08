import sys


def stdout(msg):
    sys.stdout.write(f'{msg}')
    sys.stdout.flush()


def stderr(msg):
    sys.stderr.write(f'{msg}')
    sys.stderr.flush()
