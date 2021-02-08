import os
import signal
import sys
import tty
import termios


class _GetchUnix:
    def __init__(self):
        return

    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class AlarmException(Exception):
    '''this is for unknown reasons'''
    pass


def alarmHandler(signum, frame):
    '''this also'''
    raise AlarmException


def getchar(timeout=0.15):
    '''to get input... also default is None'''
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        char = _GetchUnix()()
        signal.alarm(0)
        return char
    except AlarmException:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return None
    return None
