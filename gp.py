#!/usr/local/bin/python3

import logging
import sys, termios
from os import system

import tty
import string
import glob
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

import os
def get_all_files():
    return glob.glob("/Users/dev")


class Row:
    def __inti__(self):
        self.row = ""

    def getRowLength(self):
        return len(self.row)


class E:
    def __init__(self):
        self.w , self.h =  os.get_terminal_size()
        self.ab = []
        self.cx = 0
        self.cy = 1
        self.rows = []
        self.row = ""
        self.rowoffset = 0
        #self.rowcount = 0

    def clearBuffer(self):
        self.ab = []

    def writeBufferToScreen(self):
        #import pdb;pdb.set_trace()
        for i in self.ab:
            sys.stdout.write(i)
        sys.stdout.flush()    
    
    def get_rowcount(self):
        #return len(self.row)
        return len(self.rows) - 1

    
    #def set_rowcount(self, c):
    #    self._rowcount += c

def editorAppendRow(line):
    logger.info(line)
    e.rows.append(line)

def editorOpen(filename):
    e.row = "Hi Hello World!"
    #import pdb;pdb.set_trace()
    with open(filename) as f:
        for line in f:
            editorAppendRow(line)
        
def restoreCanonMode(fd, old):
    termios.tcsetattr(fd, termios.TCSADRAIN, old)

def enableRawMode(fd):
    new = termios.tcgetattr(fd)
    new[3] &= ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSADRAIN, new)

def readKey():
    while True:
        c = sys.stdin.read(1)
        if c == '\x1b':
            c1 = sys.stdin.read(1)
            c2 = sys.stdin.read(1)

            if c1 == '[':
                if c2 == 'A': return 'w'
                if c2 == 'B': return 's'
                if c2 == 'C': return 'd'
                if c2 == 'D': return 'a'
        else:
            return c


def editorMoveCursor(key):
    if key == 'a':
        e.cx -= 1
    if key == 'd':
        e.cx += 1
    if key == 'w':
        if e.cy > 0:
            e.cy -= 1
    if key == 's':
        if e.cy <= e.get_rowcount():
            e.cy += 1
    

def launchFileManager():
    system('clear')
    import time
    

    w = int(e.w/3)
    x= 10
    y= 30
    TOP_LEFT        =   '╔'
    TOP_RIGHT       =   '╗'
    BOTTOM_LEFT     =   '╚'
    BOTTOM_RIGHT    =   '╝'
    VERTICAL_JOIN   =   '║'
    HORIZONTAL_JOIN =   '═'
    
    #start_file_manager_x = int(w-w/2)
    sys.stdout.write('\r\n\r\n')
    sys.stdout.write(' '*x+TOP_LEFT+HORIZONTAL_JOIN*w+TOP_RIGHT+'\r\n')
    h=30
    for i in range(h):
        sys.stdout.write(' '*x+VERTICAL_JOIN+' '*w+f'{VERTICAL_JOIN}\r\n')

    sys.stdout.write(' '*x+BOTTOM_LEFT+HORIZONTAL_JOIN*w+BOTTOM_RIGHT)

    sys.stdout.flush()
    time.sleep(22000)

import types


def startDebugMode():
    logger.debug('starting Editor debugger')
    while True:
        x= input('(Editor Debugger) > ')
        
        try:
            getattr(e,x)
        except AttributeError:
            logger.debug(f'Editor has no object {x}')
        else:
            if isinstance(getattr(e,x),types.MethodType):
                logger.debug(getattr(e,x)())
            else:
                logger.debug(getattr(e,x))
                
    
def editorProcessKey():
    c = readKey()

    if c == 'q':
        raise Exception
    elif c in ['w','s','a','d']:
        editorMoveCursor(c)

    elif c == 'x':
        startDebugMode()
    else:
        insertCharAt(e.cy - 1, c, e.cx - 1)

def editorScroll():
    """
        Calculate the row offset based on cursor position
    """
    #import pdb;pdb.set_trace()
    if e.cy < e.h:
        e.rowoffset = 0
    else:
        if e.cy >  e.h:
            e.rowoffset = e.cy - e.h



def addCursorPosition():
    """
        If 
    """
    if e.cy <= e.get_rowcount():

        #print("\x1b[H")
        e.ab.append("\r\033[%d;%dH"%(e.cy,e.cx))
    else:
        e.ab.append("\r\033[%d;%dH"%(e.get_rowcount(),e.cx))
        

def refreshScreen():    
    #system('clear')
    
    editorScroll()
    
    #e.ab.append("\r\x1b[2J")
    e.ab.append("\r\x1b[H")
    #sys.stdout.write("\x1b[H")
    #import pdb;pdb.set_trace()
    drawRows()
    addCursorPosition()
    #import pdb;pdb.set_trace();
    #e.ab.append('\r\x1b[H')
    #logger.debug(e.ab)

    e.writeBufferToScreen()
    e.clearBuffer()

def insertCharAt(row_idx, char, char_idx):
    e.rows[row_idx] = e.rows[row_idx][:char_idx+1]+char+e.rows[row_idx][char_idx+1:]
    editorMoveCursor('d')

def drawRows():
    for y in range(e.h):
        #import pdb;pdb.set_trace()
        linerow = y + e.rowoffset
        if y < e.get_rowcount():
            #logger.debug(f"rows: {len(e.rows)} , 'linerow': {linerow}")
            e.ab.append(e.rows[linerow])
        #elif  y == int(e.h/2):
        #    ss = "~ 🐻 Welcome to editor 🐻 ~"
        #    msg = (int(e.w/2)-int(len(ss)/2))*" "+ss
        #    e.ab.append('\u001b[31;1m~\u001b[0m'+msg)
        elif y == e.h-1:
            msg = f"({e.cx},{e.cy})"
            status = " "*(int(e.w-1)-len(msg))+msg+" "
            e.ab.append("\u001b[1m\u001b[7m"+status+"\u001b[0m")
        else:
            e.ab.append('\u001b[31;1m~\u001b[0m\r\n')

        e.ab.append('\x1b[K')
    #import pdb; pdb.set_trace()



if __name__ == '__main__':
    
    e  = E()
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    enableRawMode(fd)
    
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        editorOpen(filename)


    while True:
        try:
            refreshScreen()
            editorProcessKey()
        except Exception as e:
            restoreCanonMode(fd, old)
            import sys
            logger.debug(str(e))
            logger.debug("restoring terminal state")
            sys.exit()


    import sys
    
    #sys.exit()






