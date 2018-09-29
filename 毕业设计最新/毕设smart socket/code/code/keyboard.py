#!/usr/bin/env python
import signal
from sys import exit
import autopy
import skywriter
import os
some_value = 0
@skywriter.flick()
def flick(start,finish):
    if start == "east":
        autopy.key.tap(autopy.key.K_LEFT)
    if start == "west":
        autopy.key.tap(autopy.key.K_RIGHT)
    if start == "north":
        autopy.key.tap(autopy.key.K_DOWN)
    if start == "south":
        autopy.key.tap(autopy.key.K_UP)
signal.pause()
