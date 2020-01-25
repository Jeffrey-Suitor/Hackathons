# Libraries
import os
import reOrderTeeth  # This program allows the user to change in what order the teeth are cleaned
import subprocess  # Used to interface with wmctrl
import random  # Used to demonstrate the visual colour changes in place of actual data
import time  # Used for sleep
import tkinter  # Used to display
from PIL import Image, ImageDraw, ImageFont, ImageTk  # Used for image processing


def main():

    # Editable variables
    patientDataDirectory = subprocess.check_output("pwd", shell=True).decode("utf-8").strip() +"/patientData/"  # Absolute path to current directory
    views = ["Buccal ", "Lingual "]
    pathToToothChart = "imageResources/toothImage.png"  # Path to empty tooth chart
    toothNames = open("toothOrder.txt")

    # Variable initialization
    toothObjectList = []
    dentalViewObjectList=[]
    notStartedFile=True

    # Tkinter Setup
    myInterface=tkinter.Tk()
    canvas=tkinter.Canvas(myInterface,width=1400,height=800,background='white')
    canvas.pack()

    # Main program
    toothList = toothNames.readlines()  # Read file containing tooth number, tooth name, and tooth cordinates on tooth chart.
    patientInfo = getPatientInfo()  # Ask the user to input patient information
    patientFolder = createFolders(patientInfo, patientDataDirectory)  # Generate patient directory

    for i in range((len(views))):
        dentalViewObjectList.append(dentalView(pathToToothChart, views[i]))  # Append views objects to list
        dentalViewObjectList[i].formatImage()  # Format each dental image to remove watermark
        dentalViewObjectList[i].createCopy()  # Create a copy of the original chart image


    for i in range(len(dentalViewObjectList)):
        toothObjectList = []
        for k in range(len(toothList)):
            tempToothList = toothList[k].split()  # List of form [number, tooth, x, y)
            tempToothList.remove(tempToothList[0])  # List of form [tooth, x, y]
            tempToothList[1] = "".join([tempToothList[1], tempToothList[2]])  # List of form [tooth, tuple(x,y), ycord]
            tempToothList.remove(tempToothList[2])  # List of form [tooth, tuple]
            toothObjectList.append(tooth(tempToothList[0], tempToothList[1], k+1))  # Append tooth, tuple, number
            toothObjectList[k].setDepth()  # Finds sets the depth of the tooth being currently worked on.
            toothObjectList[k].setColour()  # Sets the colour of the tooth based on the depth of the tooth
            while toothObjectList[k].getRepeat():  # If the data is unuseable repeat the data collection
                toothObjectList[k].setDepth()
                toothObjectList[k].setColour()
            completeImage=dentalViewObjectList[i].updatePILImage(toothObjectList[k])  # Update the image with the new tooth data
            showImage(canvas,completeImage)  # Show image
        dentalViewObjectList[i].saveCurrentViewImage(patientFolder)  # Saves an image of the finished dental view

        writeToPatientFile(notStartedFile,dentalViewObjectList[i].getImageText(),toothObjectList, patientInfo, patientFolder)  # Writes all tooth data to the patient file
        notStartedFile=False


def showImage(s, pillImage):
    tkinterImage=ImageTk.PhotoImage(pillImage)  # Convert PIL image to TKinter
    s.create_image(0, 0, anchor='nw', image=tkinterImage)  # Create image on canvas
    s.update()  # Update the canvas
    time.sleep(1)
    s.delete('all')


def getPatientInfo():
    patientInfo = []
    print('\nPlease answer the following questions before beginning a scan, press the enter key after each response.\n')
    patientInfo.append('Patient Name: ' + input('Name: '))  # patientInfo[0] = patient name
    patientInfo.append('\nDate: ' + input('Date: '))  # patientInfo[1] = date
    print('\nPatient information recorded.\n')
    return patientInfo


def writeToPatientFile(notStartedFile, text,teeth,patientInfo, patientFolder):
    filename = patientInfo[0] + "_" + patientInfo[1] + '.txt'  # Filename is patientName_Date .txt
    f = open(patientFolder + '/' + filename, 'a+')
    if notStartedFile:
        for i in range(len(patientInfo)):
            f.write(patientInfo[i])  # Writes previously inputted patient info
        f.write("\nView".ljust(41) + "Tooth".ljust(80) + "Depth\n")
    for i in range(len(teeth)):
        f.write(str(text).ljust(40) + teeth[i].getName().ljust(80) + str(teeth[i].getDepth()) + "mm\n")  # Gets tooth name and depth
    f.close()


def createFolders(patientData,patientDataDirectory):

    if not os.path.exists(patientDataDirectory):  # Creates patient data patientDataDirectory
        os.makedirs(patientDataDirectory)

    patientFolder = patientDataDirectory + patientData[0] + ":" + patientData[1]

    if not os.path.exists(patientFolder):  # Creates patient folder
        os.makedirs(patientFolder)

    return patientFolder


class tooth:

    # Constructor
    def __init__(self, name, position, number):
        self.name = name
        self.position = eval(position)  # Generates a tuple of position
        self.number = number
        self.depth = None
        self.colour = None
        self.repeat = False

    # Accessors
    def getName(self):
        return self.name

    def getDepth(self):
        return self.depth

    def getColour(self):
        return self.colour

    def getRepeat(self):
        return self.repeat

    def getPosition(self):
        return self.position

    def getNumber(self):
        return self.number

    # Mutators
    def setColour(self):
        if self.depth <= 3:
            self.colour = (9, 255, 0,  255)  # Green
        elif 3 < self.depth <= 5:
            self.colour = (255, 228, 0, 255)  # Yellow
        elif 5 < self.depth <= 7:
            self.colour = (255, 107, 0, 255)  # Orange
        elif 7 < self.depth:
            self.colour = (255, 14, 0, 255)  # Red
        else:
            self.colour = "error"
            print("There has been an error in measurement please repeat the tooth")
            self.repeat = True  # Set repeat to True

    def setDepth(self):
        possibleDepths = [1,2,3,2,3,1,4,5,7,8,6,1,2,3,3,2,1]
        self.depth = random.choice(possibleDepths)  # Randomly generate a number between 1 and 8
        #TODO add proper code and calcs to calculate distance traveled based on pressure and water displaced


class dentalView:
    # Constructor
    def __init__(self, imageLink, imageText):
        self.image = Image.open(imageLink)
        self.imageText = imageText
        self.width, self.height = self.image.size
        self.copy = None

    # Accessors
    def getImage(self):
        return self.image

    def getImageText(self):
        return self.imageText

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getCopy(self):
        return self.copy

    # Mutators
    def formatImage(self):
        self.image = self.image.crop((0, 50, self.width, self.height - 100))  # Crop top and bottom of image

    def createCopy(self):
        self.copy = self.image.copy()  # Create a copy of the tooth chart

    def addText(self):  # Add view text to center of the view
        draw = ImageDraw.Draw(self.copy)
        font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-M.ttf',80)
        draw.text(((self.getWidth()/2-200), (self.getHeight()/2)-150), self.imageText + "view", (0, 0, 0), font=font)

    def updatePILImage(self, tooth):

        img = Image.open("imageResources/" + tooth.getName() +".png")  # Open image resources of tooh

        imageData = img.getdata()  # Generate a list of pixels

        newData = []
        for RGBA in imageData:
            if RGBA[0] > 240 and RGBA[1] > 240 and RGBA[2] > 240 and RGBA[3] != 0:  # If white and not transparent
                newData.append(tooth.getColour())  # Colour the tooth based on the results of the depth test
            else:
                newData.append(RGBA)  # Else ignore and leave the pixel as it

        img.putdata(newData)  # Generate the recoloured image
        self.copy.paste(img, tooth.getPosition(), img)  #Paste the new image onto the tooth chart and maintain alpha values
        self.addText()  #Adds the text for the current view
        return self.copy  # Show the image

    def saveCurrentViewImage(self,patientFolder):
        title = patientFolder + "/" + self.imageText.strip()+"_view.png"  # Save the png with the currentView_view.png
        self.copy.save(title)


if __name__ == "__main__":
    reOrderTeeth.reOrderTeeth()  # Call the reorder teeth program
    main()
