# Sales Monitor / Tracker
# John Rei B. Enriquez
#Initiate File
""" Check Date Today
    If file for the day exists. continue monitoring and append sales to file
    if not create new file then monitor sales and append to file """

import datetime
import os
import simpleaudio as sa

try:
    from msvcrt import kbhit ,getch
except ImportError:
    import termios, fcntl, sys, os
    def kbhit():
        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
        try:
            while True:
                try:
                    c = sys.stdin.read(1)
                    return True
                except IOError:
                    return True
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

def init():
    dateLaunch = str(datetime.date.today())   #Detect Date Today
    dateLaunch = dateLaunch.split('-')        #Separete Year, Month, Day
    fileName = "".join(dateLaunch)            #Create Filename from Date

    #Check if log exists
    fileToday = os.path.isfile('./'+fileName+'.log')

    if fileToday is False:                      #If it does not exist
        logFile = open(fileName+".log", "w")    #Create file
        logFile.close()
        print("File for the day not found. File created")
    print("Initialization Done")
    return(fileName+".log")                     #return filename

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return str(msvcrt.getch())[2:3]




def soundCash():
    wave_obj = sa.WaveObject.from_wave_file("sounds/cash.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

def soundSuccess():
    wave_obj = sa.WaveObject.from_wave_file("sounds/success.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

def soundError():
    wave_obj = sa.WaveObject.from_wave_file("sounds/error.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

def waitForKey():
    startChar = '+'
    stopChar = '!'
    while True:
        if kbhit():
            key = _Getch()
            keyPressed = str(key())
            if keyPressed in startChar:
                soundCash()
                return True
            elif keyPressed == stopChar:
                return False
            else:
                print("Key pressed: " + keyPressed)
                soundError()

def monitorKeyboard():
    if waitForKey() is True:               #if START character is detected get input
        finalSalesEntry = ""
        salePrice = str(input("Price Sold: "))
        #input verification - make sure only integer is passed
        for i in salePrice:
            if i in integers:
                finalSalesEntry += i
        print("Sold " + finalSalesEntry + "php")
        #Append to file
        appendToLog(finalSalesEntry)
        printTotal()
        soundSuccess()
        return True


    else:
        print("Stopping Program")
        return False


def appendToLog(appendData):
    appendData = appendData + "," + str(datetime.datetime.now().time())
    with open(workingFile, "a") as f:
        f.write(str(appendData) + "\n")

def cleanFile():
    f = open(workingFile, "r+")
    d = f.readlines()
    f.seek(0)
    for i in d:
        if i != "\n":
            f.write(i)
    f.truncate()
    f.close()

def printTotal():
    cleanFlag = False
    priceAcc = 0
    with open(workingFile,"r+") as f:
        for line in f:
            entryList = line.split(',')
            try:
                priceAcc += int(entryList[0])
            except ValueError:
                print("An entry was null or invalid")
                #Remove null entries
                cleanFlag = True
    if cleanFlag is True:
        cleanFile()
    print("TOTAL TODAY:" + str(priceAcc) + " php")


#Start Program

integers = "1234567890"
runProgram = True
workingFile = init()

 #monitor keyboard for START character
print("Waiting for Input")
while runProgram is True:
    runProgram = monitorKeyboard()
