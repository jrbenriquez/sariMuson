import os

# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import sys
    import termios
    import atexit
    from select import select

def kbhit():
    ''' Returns True if keyboard character was hit, False otherwise.
    '''
    if os.name == 'nt':
        return msvcrt.kbhit()

    else:
        dr,dw,de = select([sys.stdin], [], [], 0)
        return dr != []


while True:

    if kbhit():
        print('Hit!!')
