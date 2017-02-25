
import tkinter
import datetime
import os
import simpleaudio as sa

class sariMusonApp(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.minsize(width=600, height=250)
        self.grid()

        self.entry = tkinter.Entry(self)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<KP_Enter>", self.OnPressEnter)
        self.entry.config(font=("Arial", 44))
        self.label = tkinter.Label(self,
                              anchor="w",fg="white",bg="blue")
        self.label.grid(column=0,row=4,columnspan=2,sticky='EW')
        self.label.config(font=("Arial", 18))
        self.labelEvent = tkinter.Label(self,
                              anchor="w",fg="white",bg="red")
        self.labelEvent.grid(column=0,row=3,columnspan=2,sticky='EW')
        self.labelEvent.config(font=("Arial", 18))

        self.labelMisc = tkinter.Label(self,
                              anchor="w",fg="black",bg="white")
        self.labelMisc.grid(column=0,row=2,columnspan=2,sticky='EW')
        self.labelMisc.config(font=("Arial", 28))

        self.labelMisc2 = tkinter.Label(self,
                              anchor="w",fg="black",bg="white")
        self.labelMisc2.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.labelMisc2.config(font=("Arial", 44))
        self.resizable(False,False)

    def addFunction(self,event=None):
        soundCash()
        self.label['text'] = 'Add'
        self.entry.focus()
    def subFunction(self,event=None):
        soundCash()
        self.label['text'] = 'Subtract'
        self.entry.focus()
    def OnPressEnter(self,event):
        inputText = self.entry.get()
        cleanInput = parseInput(inputText)
        print(inputText,cleanInput)
        self.entry.delete(0,'end')
        print(self.label['text'])
        currentCommand = self.label['text']
        if currentCommand == "Add":
            appendToLog(cleanInput)
            self.labelEvent['text']= "Benta: "+ cleanInput +" php"
        if currentCommand == "Subtract":
            cleanInput = "-" + cleanInput
            appendToLog(cleanInput)
            self.labelEvent['text']= "Bawas: "+ cleanInput +" php"
        printTotal(self)

        self.labelMisc['text'] = datetime.datetime.now().strftime('%I:%M:%S')

        self.label.focus()
def parseInput(inputText):
    integers = "1234567890"
    finalEntry = ""
    for i in inputText:
        if i in integers:
            finalEntry += i
    return finalEntry    
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

def soundCash(*event):
    print(event)
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


def printTotal(self):
    cleanFlag = False
    priceAcc = 0
    with open(workingFile,"r+") as f:
        for line in f:
            entryList = line.split(',')
            try:
                priceAcc += int(entryList[0])
                self.labelMisc['text']=""
            except ValueError:
                self.labelMisc['text']="An entry was null or invalid"
                #Remove null entries
                cleanFlag = True
    if cleanFlag is True:
        cleanFile()
    self.labelMisc2['text'] = "TOTAL:" + str(priceAcc) + " php"

if __name__ == "__main__":
    workingFile = init()
    app = sariMusonApp(None)
    app.title('sariMuson')
    app.bind("<KP_Add>", app.addFunction)
    app.bind("<KP_Subtract>", app.subFunction)
    app.mainloop()
