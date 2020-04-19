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
from lex_py import LEX_PYTHON
import os
import traceback

from theme_default import THEME_MAP

def get_all_files():
    return glob.glob("/Users/dev")

class Row:
    def __inti__(self):
        self.row = ""

    def getRowLength(self):
        return len(self.row)

from enum import Enum

from editorKeys import Keys


class EditorModes(Enum):
    INSERT = 'INSERT'
    VISUAL = 'VISUAL'
    



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
        self.mode = EditorModes.VISUAL

    
    def change_mode(self, mode):
        self.mode = mode

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



def highlight(tokens, source_rows):
    
    default = "\u001b[0m"
    
    highlighted_token= ""
    highlighted_line =''
    
    rows = []     
    for token in tokens:
        
        if token.type.name == 'NEWLINE':
            highlighted_line += '\n'
            rows.append(highlighted_line)
            highlighted_line = ''
        else:
            
            if token.row_start != token.row_end:
                # highlight token from where it starts on the first row (out of total rows to which this token spans)

                token_string = source_rows[token.row_start][token.col_start:]
                
                for i in range(token.row_start+1, token.row_end):
                    token_string += source_rows[i]
                
                # highlight the last row of the multiline spannign token (ex, triple quotes in `"""` python   )
                token_string += source_rows[token.row_end][:token.col_end+1] + default
                
            else:
                token_string =  source_rows[token.row_start][token.col_start:token.col_end+1]
            
            if THEME_MAP.get(token.type.name, None):
                token_string = THEME_MAP[token.type.name] + token_string + default
            highlighted_line += token_string
    #p(rows)
    return rows 
    





def editorOpen(filename):
    e.row = "Hi Hello World!"
    rows = []
    
    with open(filename) as f:
        source = f.read()
        rows = [line+'\n' for line in source.split('\n')]
    tokens = LEX_PYTHON(source).lex()
    
    #rows = highlight(tokens, rows)
    
    for row in rows:
        editorAppendRow(row)

   
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
                if c2 == 'A': return Keys.TOP
                if c2 == 'B': return Keys.DOWN
                if c2 == 'C': return Keys.RIGHT
                if c2 == 'D': return Keys.LEFT
        else:
            return c

def get_logical_index(x,y):
    """
        The physical position of cursor {x,y} has to be mapped to the logical position of append_buffer,
        physical screen top left is at {1,1} & append buffer array starts at index 0.
    """
    return (x-1, y-1)

def insertCharAt(cursor_x, cursor_y, char):
    """
        Recieves the logical physical position of the cursor & the character to insert
    """

    # Find the actual position to add in the append buffer.
    col_idx, row_idx = get_logical_index(cursor_x, cursor_y )
    
    if char == "\n":
        #check if the split has to be done
        if len(e.rows[row_idx]) == col_idx:
            e.rows = e.rows[:row_idx+1]+['\n']+e.rows[row_idx+1:]
            editorMoveCursor(Keys.DOWN)
        else:
            new_row = e.rows[row_idx][col_idx:]
            current_row = e.rows[row_idx][:col_idx]
            e.rows[row_idx] = current_row
            e.rows = e.rows[:row_idx+1]+['\n']+[new_row]+['\n']+e.rows[row_idx+1:]
            editorMoveCursor(Keys.DOWN)
    
    elif ord(char) == 127:
        e.rows[row_idx] = e.rows[row_idx][:col_idx - 1 ]+e.rows[row_idx][col_idx:]
        editorMoveCursor(Keys.LEFT)

    else:
        e.rows[row_idx] = e.rows[row_idx][:col_idx]+char+e.rows[row_idx][col_idx:]
        editorMoveCursor(Keys.RIGHT)

def editorMoveCursor(key,units=1):
    
    col_idx, row_idx = get_logical_index(e.cursor_x, e.cursor_y )
    
    if key == Keys.LEFT:
        if e.cursor_x > 1:
            e.cursor_x -= units
    if key == Keys.RIGHT:

        if e.cursor_x < len(e.rows[row_idx]):
            e.cursor_x += units
    if key == Keys.TOP:
        
        # Check if there is any character directly in above row, if so move cursor to that position , 
        # otherwise move cursor to the end of previous line

        if e.cursor_y > 1:
            if len(e.rows[row_idx - 1]) < len(e.rows[row_idx]):
                e.cursor_x = len(e.rows[row_idx - 1])
            e.cursor_y -= units
            
    if key == Keys.DOWN:
        # Check if there is any character directly below the current cursor, if so move cursor to that position,
        # otherwise move cursor to the end of next line
        if e.cursor_y <= e.get_rowcount():
            if len(e.rows[row_idx + 1]) < len(e.rows[row_idx]):
                e.cursor_x = len(e.rows[row_idx + 1])
            e.cursor_y += units
    

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
    
    if c in [Keys.LEFT, Keys.RIGHT, Keys.TOP, Keys.DOWN]:
        editorMoveCursor(c)
    
    elif e.mode == EditorModes.VISUAL:
        if c == 'i':
            e.change_mode(EditorModes.INSERT)
    elif c == 'x': raise Exception
    else:
        if e.mode == EditorModes.INSERT:
            insertCharAt(e.cursor_x, e.cursor_y, c)




def editorScroll():
    """
        Calculate the row offset based on cursor position
    """
    if e.cursor_y < e.height:
        e.rowoffset = 0

    if e.cursor_y >= e.height:
        e.rowoffset = e.cursor_y - e.height


def refreshScreen(editor):
    """ refreshes the screen of the editor instance passed.
    :param editor Editor instance that is to be refreshed.
    """

    editorScroll()
    
    '''Add the action `move to start of terminal windows` to the append buffer'''
    editor.append_buffer.append("\r\x1b[H")
    
    drawRows(editor)

    editor.append_buffer.append("\r\033[%d;%dH"%(editor.cursor_y,editor.cursor_x))
    editor.writeBufferToScreen()
    editor.clearBuffer()


def drawRows(e):
    

    # NOTE: Change background color for texts to solarized for now, Make it themable later on
    #e.append_buffer.append("\u001b[48;5;15m")
    

    # ALl lines on the screen should be drawn in this loop
    

    for y in range(e.height):
        e.append_buffer.append('\x1b[K')
        linerow = y + e.rowoffset

        # NOTE : e.height - 2 as last line has to be for the status bar & row indes starts at 0 so e.height - 1 - 1
        if y < e.get_rowcount() and y < e.height - 2:
            e.append_buffer.append(e.rows[linerow])
        
        elif  y == int(e.height/2) and e.get_rowcount() <=0 :
            ss = "~ 🐻 welcome to the editor 🐻 ~"
            msg = (int(e.width/2)-int(len(ss)/2))*" "+ss+"\r\n"
            e.append_buffer.append('~'+msg)
        
        elif y == e.height - 1 :
            msg = f"({e.cursor_x},{e.cursor_y})"
            mode = f"[{e.mode.name}]"
            status = " "*(int(e.width-2)-len(msg)-len(mode))+mode+" "+msg+" "
            e.append_buffer.append("\u001b[48;5;2m"+status+"\u001b[0m")

        else:
            e.append_buffer.append('~\r\n')





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
            logger.debug(traceback.format_exc())
            logger.debug("restoring terminal state")
            sys.exit()


    import sys
    
    #sys.exit()






