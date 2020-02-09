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


class Editor:
    def __init__(self, width=0, height=0, append_buffer=[], cursor_x=0, cursor_y=0, rows=[], row='', rowoffset=0):
        """ 
        represents an editor & all associated functions.
        :param width: the width of the editor's editable area.
        :param height: the height of the editor's editable area.
        :param append_buffer: buffer used to represent screen contents in memory.
        :param cursor_x: cursor's initial horizontal position (default x=>1 is at column 1).
        :param cursor_y: cursor's initial vertical position (default x=>2 is at column 2).
        :param rows: contains rows of the editor.
        :param rowoffest: offset from row of cursor.
        """
        
        self.width = width
        self.height = height  #os.get_terminal_size()
        self.append_buffer = []
        self.cursor_x = 1
        self.cursor_y = 1
        self.rows = []
        self.row = ""
        self.rowoffset = 0



    def clearBuffer(self):
        self.append_buffer = []

    def writeBufferToScreen(self):
        for i in self.append_buffer:
            sys.stdout.write(i)
        sys.stdout.flush()    
    
    def get_rowcount(self):
        return len(self.rows)


def editorAppendRow(line):
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
        e.cursor_x -= 1
    if key == 'd':
        e.cursor_x += 1
    if key == 'w':
        e.cursor_y -= 1
    if key == 's':
        e.cursor_y += 1
    

def launchFileManager():
    system('clear')
    import time
    

    w = int(e.width/3)
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
    if c in ['w','s','a','d']:
        editorMoveCursor(c)
    if c == 'f':
        launchFileManager()
    if c == 'x':
        startDebugMode()


def editorScroll():
    """
        Calculate the row offset based on cursor position
    """
    if e.cursor_y < e.rowoffset:
        e.rowoffset = e.cursor_y
    if e.cursor_y >= e.rowoffset + e.height:
        e.rowoffset = e.cursor_y - e.height


def refreshScreen(editor):
    """ refreshes the screen of the editor instance passed.
    :param editor Editor instance that is to be refreshed.
    """

    '''Add the action `move to start of terminal windows` to the append buffer'''
    editor.append_buffer.append("\r\x1b[H")
    
    drawRows(editor)

    editor.append_buffer.append("\r\033[%d;%dH"%(editor.cursor_y,editor.cursor_x))
    #logger.debug(editor.append_buffer)
    editor.writeBufferToScreen()
    editor.clearBuffer()


def drawRows(e):
    for y in range(e.height):
        #import pdb;pdb.set_trace()
        linerow = y + e.rowoffset
        if y < e.get_rowcount():
            e.append_buffer.append(e.rows[linerow])
        elif  y == int(e.height/2):
            ss = "~ 🐻 welcome to the editor 🐻 ~"
            msg = (int(e.width/2)-int(len(ss)/2))*" "+ss+"\r\n"
            e.append_buffer.append('~'+msg)
        elif y == e.height - 2:
            cursor_positions = f"({e.cursor_x}, {e.cursor_y})\r\n"
            e.append_buffer.append(cursor_positions)
        else:
            e.append_buffer.append('~\r\n')
        e.append_buffer.append('\x1b[K')

if __name__ == '__main__':
    
    main_window_width, main_window_height = os.get_terminal_size()
    
    #main_window_width, main_window_height = (10,10)
    e  = Editor(width=main_window_width, height=main_window_height)
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    enableRawMode(fd)
    
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        editorOpen(filename)


    while True:
        try:
            refreshScreen(e)
            editorProcessKey()
        except Exception as e:
            restoreCanonMode(fd, old)
            import sys
            logger.debug(str(e))
            logger.debug("restoring terminal state")
            sys.exit()


    import sys
    
    #sys.exit()






