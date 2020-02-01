

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

