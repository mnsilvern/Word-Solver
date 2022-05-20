#------------------------------------------------------------------------------
#from WS
#from collections import Counter

#import copy

#import your functions file
from functions import *

#------------------------------------------------------------------------------
#from GUI  import Ui_MainWindow #Import generated class from the gui file
from PyQt5 import QtWidgets, uic, QtGui, QtCore

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton
import sys

enterLettersText = 'Enter your guess and a color for each letter'
colorErrorText = 'Please ensure each letter has been assigned a color.'
solvingText = 'Solving...'
roundExceededText = 'Round number is exceeded'


numCharacters = 5
#------------------------------------------------------------------------------
#gui function start
def colorPress(colorNumReceive):
    #textEdit Color
    
    brushGrey = [[58, 58, 60],[58, 58, 60],[43, 213, 173]]
    brushYellow = [[144, 144, 0], [144, 144, 0], [166, 58, 172]]
    brushGreen = [[83, 141, 78],[83, 141, 78],[68, 40, 191]]
    brushBlack = [[18, 18, 19],[18, 18, 19],[173, 173, 173]]
    
    brushDict = {
        0: brushGrey,
        1: brushYellow,
        2: brushGreen,
        -1: brushBlack
        }
    
    return brushDict[colorNumReceive]

#------------------------------------------------------------------------------
#Window start

#Class for the main window that inherits 
# from the QT creator auto-generated class
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        
        #load ui
        uic.loadUi("rawGUI.ui", self)
        
        #define our widgets
        self.label = self.findChild(QLabel, "label")
        self.lineEdit1 = self.findChild(QLineEdit, "lineEdit1")
        self.lineEdit2 = self.findChild(QLineEdit, "lineEdit2")
        self.lineEdit3 = self.findChild(QLineEdit, "lineEdit3")
        self.lineEdit4 = self.findChild(QLineEdit, "lineEdit4")
        self.lineEdit5 = self.findChild(QLineEdit, "lineEdit5")
        self.pushButtonSubmit = self.findChild(QPushButton, "pushButtonSubmit")
        self.pushButton1 = self.findChild(QPushButton, "pushButton1")
        self.pushButton2 = self.findChild(QPushButton, "pushButton2")
        self.pushButton3 = self.findChild(QPushButton, "pushButton3")
        self.pushButton4 = self.findChild(QPushButton, "pushButton4")
        self.pushButton5 = self.findChild(QPushButton, "pushButton5")
        
        #do things
        self.pushButtonSubmit.clicked.connect(self.submitPressed)
        
        #pushButtons to change color
        self.color1 = -1
        self.color2 = -1
        self.color3 = -1
        self.color4 = -1
        self.color5 = -1
        
        self.colorSet = [self.color1, self.color2, self.color3, self.color4, self.color5]
        
        #connect 'change color' buttons to methods
        self.pushButton1.clicked.connect(self.color1Pressed)
        self.pushButton2.clicked.connect(self.color2Pressed)
        self.pushButton3.clicked.connect(self.color3Pressed)
        self.pushButton4.clicked.connect(self.color4Pressed)
        self.pushButton5.clicked.connect(self.color5Pressed)
        
        #grab initial content of each letter
        self.char1 = self.lineEdit1.text()
        self.char2 = self.lineEdit2.text()
        self.char3 = self.lineEdit3.text()
        self.char4 = self.lineEdit4.text()
        self.char5 = self.lineEdit5.text()
        
        #define contents as list for ease
        self.charSet = [self.char1, self.char2, self.char3, self.char4, self.char5]

        #define the boxes as a list for ease
        self.boxSet = [self.lineEdit1, self.lineEdit2, self.lineEdit3, self.lineEdit4, self.lineEdit5]
        
        #set initial focus to box1
        self.boxSet[0].setFocus()
        self.boxSet[0].selectAll()
        
        #set up keypress handlers to detect user input
        for c in self.boxSet:
            c.textEdited.connect(self.inputKeyUp)
        
#------------------------------------------------------------------------------        
#wordleBot variables
        #set variables for wordleBot
        self.round = -1
        
        self.numCharacters = 5
        self.spaceReduction = .25
        self.printNum = 5
        self.roundNum = 6
        self.wordSource = 'wordleList.txt'
        #self.wordSource = 'wordleLegalGuess.txt'
        
        self.goodSetMade = []
        self.greySetMade = []
        self.yellowSetMade = [[] for _ in range(self.numCharacters)]
        self.greenSetMade = [[] for _ in range(self.numCharacters)]
        
        with open(self.wordSource,'r') as f:
            self.wordleList = f.readlines()
        self.charNListNoPN = [s.replace("\n", "") for s in self.wordleList]

        #from WS
        #word space
        self.wordSpaceList = [0]*(self.roundNum+1)
        self.wordSpaceList[0] = len(self.charNListNoPN)
        
#------------------------------------------------------------------------------
        #show the app
        self.show()
    
#------------------------------------------------------------------------------
#method start
    #move forward, backwards, or stay put upon keypress
    def inputKeyUp(self):
        #take the current state of the letters
        char1Temp = self.lineEdit1.text()
        char2Temp = self.lineEdit2.text()
        char3Temp = self.lineEdit3.text()
        char4Temp = self.lineEdit4.text()
        char5Temp = self.lineEdit5.text()
        
        #group them for ease
        charSetTemp = [char1Temp, char2Temp, char3Temp, char4Temp, char5Temp]
        
        #grab current focused box
        boxFocus = QtWidgets.QApplication.focusWidget()
        
        #either advance, retract, or remain based on input and position
        for boxNum in range(len(self.boxSet)):
            if boxFocus == self.boxSet[boxNum]:
                currentBoxIndex = boxNum
                #advance if not '' and 
                if charSetTemp[boxNum] != '' and boxNum < len(self.boxSet) - 1:
                    nextBoxIndex = currentBoxIndex + 1
                #stay put if not '' and at last letter
                elif charSetTemp[boxNum] != '' and boxNum == len(self.boxSet) - 1:
                    nextBoxIndex = currentBoxIndex
                #retract if "" and not at beginning
                elif charSetTemp[boxNum] == '' and boxNum > 0:
                    nextBoxIndex = currentBoxIndex - 1
                elif charSetTemp[boxNum] == '' and boxNum == 0:
                    nextBoxIndex = currentBoxIndex
        
        #remember the focus box, select next focus box, highlight it
        self.boxSet[nextBoxIndex].setFocus()
        self.boxSet[nextBoxIndex].selectAll()
        
        #reset box contents
        self.char1 = self.lineEdit1.text()
        self.char2 = self.lineEdit2.text()
        self.char3 = self.lineEdit3.text()
        self.char4 = self.lineEdit4.text()
        self.char5 = self.lineEdit5.text()
                    
        self.charSet = [self.char1, self.char2, self.char3, self.char4, self.char5] 

    def submitPressed(self):
    #where most of the magic happens
        #retrieve contents from boxes and lowercase them
        self.char1 = self.lineEdit1.text().lower()
        self.char2 = self.lineEdit2.text().lower()
        self.char3 = self.lineEdit3.text().lower()
        self.char4 = self.lineEdit4.text().lower()
        self.char5 = self.lineEdit5.text().lower()
        
        self.charSet = [self.char1, self.char2, self.char3, self.char4, self.char5] 
        
        #lists to contain guess letters
        self.greyGuess = list(' ' * numCharacters)
        self.yellowGuess = list(' ' * numCharacters)
        self.greenGuess = list(' ' * numCharacters)
        
        #define dictionary for colorMod codes
        self.colorCodeDict ={
            0: self.greyGuess,
            1: self.yellowGuess,
            2: self.greenGuess
            }
        
        #gather up current color values
        self.colorSet = [self.color1, self.color2, self.color3, self.color4, self.color5]
        
        #check for uncolored box
        colorError = 0
        for colorNum in self.colorSet:
            if colorNum == -1:
                colorError = 1
        
        #error if uncolored box, otherwise proceed
        if colorError == 1:
            self.label.setText(colorErrorText)
        else:
            self.label.setText(solvingText)
            self.repaint()
            #consolidate colorMods
            self.colorModSet = [self.color1Mod, self.color2Mod, self.color3Mod, self.color4Mod, self.color5Mod]
            #assign each letter to a position in the color guess sets
            for modStep in range(len(self.colorModSet)):
                self.colorCodeDict[self.colorModSet[modStep]][modStep] = self.charSet[modStep]
            
            #join color guess sets, format for wordleBot handling
            for dictSet in self.colorCodeDict:
                self.colorCodeDict[dictSet] = ["".join(self.colorCodeDict[dictSet])]
            #can be removed
            
            #firmly define them
            self.greyGuess = self.colorCodeDict[0]
            self.yellowGuess = self.colorCodeDict[1]
            self.greenGuess = self.colorCodeDict[2]
            
            # #testCode
            # print(self.greyGuess)
            # print(self.yellowGuess)
            # print(self.greenGuess)
            
#------------------------------------------------------------------------------
            #wordleBot start
            if self.round >= 6:
                print(roundExceededText)
            self.round = self.round + 1
    
            self.greySetMade = greyLet(self.greySetMade,self.greyGuess)
            self.goodSetMade,self.yellowSetMade = yellowLet(self.goodSetMade,self.yellowSetMade,self.yellowGuess)
            self.goodSetMade,self.greenSetMade = greenLet(self.goodSetMade,self.greenSetMade,self.greenGuess)
            self.greyListMade,self.goodListMade,self.yellowListMade,self.greenListMade = guessListMaker(self.numCharacters,self.charNListNoPN,self.goodSetMade,self.greySetMade,self.yellowSetMade,self.greenSetMade)
            
            self.wordSpaceList[self.round+1] = len(self.greenListMade)
            
            self.wordUncAvgListSorted = wordUnc(self.numCharacters,self.greenListMade,self.greenListMade,self.greenSetMade,self.yellowSetMade,self.greySetMade,self.goodSetMade)
            
            print('--------------------------------------')
            
            print('space size history: ' + str(self.wordSpaceList))
            
            if (min(self.wordUncAvgListSorted)[0] >= self.spaceReduction*self.wordSpaceList[self.round+1]) and (self.wordSpaceList[self.round+1] > 2):
                self.wordUncAvgListSorted = wordUnc(self.numCharacters,self.yellowListMade,self.greenListMade,self.greenSetMade,self.yellowSetMade,self.greySetMade,self.goodSetMade)
                print('estimated new space size: ' + str(min(self.wordUncAvgListSorted)[0]))
                print('yellowList used')
            else:
                print('estimated new space size: ' + str(min(self.wordUncAvgListSorted)[0]))
                print('greenList used')
            
            print('\n')
            
            if len(self.wordUncAvgListSorted) <= 5:
                self.printNum = len(self.wordUncAvgListSorted)
            for i in range(self.printNum):
                print(self.wordUncAvgListSorted[i])
            
#------------------------------------------------------------------------------
#update gui
            if len(self.wordUncAvgListSorted) > 0:
                self.nextWord = self.wordUncAvgListSorted[0]
                #print(self.nextWord[1])
            
            #time to reset the GUI with the new letters
            self.colorModReset = -1
            self.resetBrush = colorPress(self.colorModReset)
            for boxReset in range(len(self.boxSet)):
                
                #fill box with appropriate next letter
                self.boxSet[boxReset].setText(self.nextWord[1][boxReset])
                
                #change background color to match returned color
                #active brush, text
                palette = QtGui.QPalette()
                brush = QtGui.QBrush(QtGui.QColor(self.resetBrush[0][0], self.resetBrush[0][1], self.resetBrush[0][2]))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
                
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
                
                #inactive brush, text
                brush = QtGui.QBrush(QtGui.QColor(self.resetBrush[1][0], self.resetBrush[1][1], self.resetBrush[1][2]))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
                
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
                
                #disabled brush, text
                brush = QtGui.QBrush(QtGui.QColor(self.resetBrush[2][0], self.resetBrush[2][1], self.resetBrush[2][2]))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
                
                brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                brush.setStyle(QtCore.Qt.SolidPattern)
                palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
                
                #paint the boxes to black
                self.boxSet[boxReset].setPalette(palette)
                
                #reset box color values
                self.color1 = -1
                self.color2 = -1
                self.color3 = -1
                self.color4 = -1
                self.color5 = -1
                
            #reset label text
            self.label.setText(enterLettersText)
            
            #set initial focus to box1
            self.boxSet[0].setFocus()
            self.boxSet[0].selectAll()

#------------------------------------------------------------------------------
        


    #letter color changes
    def color1Pressed(self):
        self.color1 = self.color1 + 1
        self.color1Mod = self.color1 % 3
        color1Brush = colorPress(self.color1Mod)
        
        #self.label.setText(str(color1Brush))
        
        #change background color to match returned color
        #active brush, text
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(color1Brush[0][0], color1Brush[0][1], color1Brush[0][2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        
        #inactive brush, text
        brush = QtGui.QBrush(QtGui.QColor(color1Brush[1][0], color1Brush[1][1], color1Brush[1][2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        
        #disabled brush, text
        brush = QtGui.QBrush(QtGui.QColor(color1Brush[2][0], color1Brush[2][1], color1Brush[2][2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        
        #paint the box
        self.lineEdit1.setPalette(palette)

    def color2Pressed(self):
        self.color2 = self.color2 + 1
        self.color2Mod = self.color2 % 3
        color2Brush = colorPress(self.color2Mod)
        
        #self.label.setText(str(color2Brush))
        
        #change background color to match returned color
        #active brush, text
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(color2Brush[0][0], color2Brush[0][1], color2Brush[0][2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        
        #inactive brush, text
        brush = QtGui.QBrush(QtGui.QColor(color2Brush[1][0], color2Brush[1][1], color2Brush[1][2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        
        #disabled brush, text
        brush = QtGui.QBrush(QtGui.QColor(color2Brush[2][0], color2Brush[2][1], color2Brush[2][2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        
        #paint the box
        self.lineEdit2.setPalette(palette)
        
    def color3Pressed(self):
        self.color3 = self.color3 + 1
        self.color3Mod = self.color3 % 3
        color3Brush = colorPress(self.color3Mod)
        
        #self.label.setText(str(color3Brush))
        
        #change background color to match returned color
        #active brush, text
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(color3Brush[0][0], color3Brush[0][1], color3Brush[0][2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        
        #inactive brush, text
        brush = QtGui.QBrush(QtGui.QColor(color3Brush[1][0], color3Brush[1][1], color3Brush[1][2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        
        #disabled brush, text
        brush = QtGui.QBrush(QtGui.QColor(color3Brush[2][0], color3Brush[2][1], color3Brush[2][2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        
        #paint the box
        self.lineEdit3.setPalette(palette)
        
    def color4Pressed(self):
        self.color4 = self.color4 + 1
        self.color4Mod = self.color4 % 3
        color4Brush = colorPress(self.color4Mod)
        
        #self.label.setText(str(color4Brush))
        
        #change background color to match returned color
        #active brush, text
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(color4Brush[0][0], color4Brush[0][1], color4Brush[0][2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        
        #inactive brush, text
        brush = QtGui.QBrush(QtGui.QColor(color4Brush[1][0], color4Brush[1][1], color4Brush[1][2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        
        #disabled brush, text
        brush = QtGui.QBrush(QtGui.QColor(color4Brush[2][0], color4Brush[2][1], color4Brush[2][2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        
        #paint the box
        self.lineEdit4.setPalette(palette)
        
    def color5Pressed(self):
        self.color5 = self.color5 + 1
        self.color5Mod = self.color5 % 3
        color5Brush = colorPress(self.color5Mod)
        
        #self.label.setText(str(color5Brush))
        
        #change background color to match returned color
        #active brush, text
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(color5Brush[0][0], color5Brush[0][1], color5Brush[0][2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        
        #inactive brush, text
        brush = QtGui.QBrush(QtGui.QColor(color5Brush[1][0], color5Brush[1][1], color5Brush[1][2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        
        #disabled brush, text
        brush = QtGui.QBrush(QtGui.QColor(color5Brush[2][0], color5Brush[2][1], color5Brush[2][2]))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        
        #paint the box
        self.lineEdit5.setPalette(palette)

#------------------------------------------------------------------------------
#main start
#Create the QT app

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
