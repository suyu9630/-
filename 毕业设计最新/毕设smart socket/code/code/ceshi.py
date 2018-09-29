import signal
from sys import exit
import autopy
import skywriter
import os
width, height = autopy.screen.get_size()
@skywriter.touch()
def touch(position):
    if(position=='south'):
        print("broadcast music")
        os.system('mplayer 2233.mp3')
        if(position=='north'):
            print('pause')
@skywriter.flick()
def flick(start,finish):
    print(start, finish)
    if(start=='west' and finish=='east'):
        print("play music")
        os.system('mplayer 1122.mp3')
        if(position=='north'):
            print('stop')
@skywriter.double_tap()
def doubletap(position):
    print('Double tap!', position)


