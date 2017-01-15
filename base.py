# Sales Monitor / Tracker
# John Rei B. Enriquez
#Initiate File
""" Check Date Today
    If file for the day exists. continue monitoring and append sales to file
    if not create new file then monitor sales and append to file """

import datetime
import os
import msvcrt
import winsound

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

def soundCash():
    winsound.PlaySound('sounds/cash.wav', winsound.SND_FILENAME)

def soundSuccess():
    winsound.PlaySound('sounds/success.wav', winsound.SND_FILENAME)

def soundError():
    winsound.PlaySound('sounds/error.wav', winsound.SND_FILENAME)
def waitForKey():
    startChar = '+'
    stopChar = '!'
    while True:
        if msvcrt.kbhit():
            key = str(msvcrt.getch())[2:3]
            if key in startChar:
                soundCash()
                return True
            elif key == stopChar:
                return False
            else:
                print("Key pressed: " + key)
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

def printTotal():
    cleanFlag = False
    priceAcc = 0
    with open(workingFile,"r+") as f:
        for line in f:
            try:
                priceAcc += int(line)
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
