import sys, os, difflib, subprocess, string, ftplib, time, getpass, telnetlib, ipaddress
from os import path
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLabel, \
    QListWidget, QListWidgetItem, QColorDialog, QLineEdit, QFileDialog, QMessageBox, QDialog, QInputDialog, QTableView, \
    QFileSystemModel, QTreeView, QComboBox, QSizePolicy, QLayout, QSpacerItem, QHBoxLayout, QFrame, QGroupBox, \
    QTableWidget, QTextBrowser, QMdiSubWindow
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5.QtCore import QUrl
from fileinput import filename
from ftplib import FTP
from typing import Any, Union
from PyQt5.QtCore import Qt, QRect  


class AllowHyperLinks(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.setOpenExternalLinks(True)
        self.setParent(parent)


class allTheThings(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(allTheThings, self).__init__(parent)

        self.checkBoxStore = []                                                                                                                 # Stores state of the checkboxes
        self.availableDrives = []
        self.gradeCheckStore = []
        self.folderChosen = ""


        self.mainTabWidget = QtWidgets.QTabWidget()  # Creates the tabs
        self.mainWindow = QtWidgets.QWidget()  # Creates tab 1
        self.compare = QtWidgets.QTabWidget()
        self.importWindow = QtWidgets.QWidget()  # Creates a Widget
        self.compareWindow = QtWidgets.QWidget()  # Creates a Widget
        self.compareOutput = QtWidgets.QWidget()  # Creates a Widget
        self.networkWindow = QtWidgets.QTabWidget()
        self.telnetWindow = QtWidgets.QWidget()  # Creates a Widget (RM)
        self.mapFolder = QtWidgets.QWidget()  # Creates a Widget (RM)
        self.ftpWindow = QtWidgets.QWidget()  # Creates a Widget (RM)
        self.settingsWindow = QtWidgets.QWidget()  # Creates tab 7
        self.helpWindow = QtWidgets.QWidget()
        self.gradingWindow = QtWidgets.QWidget()

        self.mainTabWidget.addTab(self.mainWindow, "Main")  # Makes tab 1 view-able
        self.mainTabWidget.addTab(self.importWindow, "Import")  # Makes tab 2 view-able
        self.mainTabWidget.addTab(self.compare, "Compare")  # Makes tab 3 view-able
        self.mainTabWidget.addTab(self.networkWindow, "Networking")  # Makes tab 4 view-able
        self.mainTabWidget.addTab(self.gradingWindow, "Grading")  # Makes tab 5 view-able
        #self.mainTabWidget.addTab(self.settingsWindow, "Settings")  # Makes tab 7 view-able
        #self.mainTabWidget.addTab(self.helpWindow, "Help")  # Makes tab 8 viewable.

        self.compare.addTab(self.importWindow, "Import")  # Makes sub-tab in Compare view-able (RM)
        self.compare.addTab(self.compareOutput, "Compare")  # Makes sub-tab in Compare view-able (RM)
        self.networkWindow.addTab(self.telnetWindow, "Telnet")  # Makes sub-tab in Network view-able (RM)
        self.networkWindow.addTab(self.ftpWindow, "FTP")  # Makes in Network view-able (RM)
        self.networkWindow.addTab(self.mapFolder, "Map Drive")  # Makes in Network view-able (RM)

        self.setWindowTitle("Quagga")                                                                                                           # Sets the window title
        self.setWindowIcon(QIcon('Qlogo.png'))
        self.setCentralWidget(self.mainTabWidget)
        
        self.spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)  # To make buttons on far left side
        self.spacer4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  # To make buttons on far left side
        self.spacer2 = QSpacerItem(400, 0, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

        logoLabel = QLabel()
        pixmap = QPixmap('Qlogo.png')
        logoLabel.setPixmap(pixmap)

        self.mainWindow.layout = QtWidgets.QVBoxLayout(self)                                                                                    # Initializes layout for tab mainWindow
        #linkTemplate = '<a href={0}>{1}</a>'                                                                                                    # Template for the link? idek
        #self.labelWebsite = AllowHyperLinks(self)                                                                                               # Makes a variable to reference AllowHyperLinks class
        #self.labelWebsite.setText(linkTemplate.format('https://Google.com',
        #                                              'Google'))                                                                                # Sets the text of the label to display our website -> replace the https://Google.com with our URL and replace Google with the text to display
        self.mainWindow.layout.addWidget(logoLabel)                                              
        #self.mainWindow.layout.addWidget(self.labelWebsite)                                                                                     # Adds the Hyperlink to the mainWindow
        self.mainWindow.setLayout(self.mainWindow.layout)
        self.mainWindow.layout.addItem(self.spacer)  # Line add RM to move everything to far left side                                                                                      # Sets the layout of the mainWindow Window



        self.importWindow.layout = QtWidgets.QVBoxLayout(self)  # Initializes layout for tab importWindow
        self.btnChangeFolder = QtWidgets.QPushButton("Choose a folder",
                                                     clicked=self.readFolder)  # Makes a button on importWindow that says "Choose a folder" then runs readFolder function
        self.btnChangeToCompare = QtWidgets.QPushButton("Compare",
                                                        clicked=self.importToCompare)  # Makes a button on importWindow that says "Compare" then runs importToCompare function
        self.importWindow.layout.addWidget(self.btnChangeFolder,
                                           alignment=QtCore.Qt.AlignLeft)  # Adds btnChangeFolder to importWindow window, aligns it to left side
        self.importWindow.layout.addWidget(self.btnChangeToCompare,
                                           alignment=QtCore.Qt.AlignLeft)  # Adds btnChangeToCompare to importWindow window, aligns it to left side

        self.importWindow.setLayout(self.importWindow.layout)  # sets the layout of importWindow window
        self.importWindow.layout.addItem(self.spacer)  # Line add RM to move everything to far left side

        self.compareWindow.setGeometry(0, 0, 200, 150)
        self.compareWindow.layout = QHBoxLayout(self)  # Initializes layout for tab compareWindow
        self.compareWindow.setContentsMargins(0, 0, 0, 280)
        self.btnAnotherCompare = QtWidgets.QPushButton("New Compare",
                                                       clicked=self.removeCompareBoxes)  # Makes a button on compareWindow that says "New Compare" then runs compareToImport function
        self.compareWindow.setLayout(self.compareWindow.layout)  # sets the layout of compareWindow window

        self.compareOutput.layout = QHBoxLayout(self)
        self.compareOutput.setContentsMargins(0, 0, 0, 0)
        self.compareOutput.setLayout(self.compareOutput.layout)

        self.telnetWindow.layout = QtWidgets.QHBoxLayout(self)
        self.telnetWindow.layout.setContentsMargins(0, 60, 0, 0)
        self.nameHost = QLabel("Enter your device IPv4: ", self.telnetWindow)  # Creates a Hostname Label (RM)
        self.nameHost.adjustSize()
        self.nameHost.move(10, 30)  # Moves it to desire location (RM)
        self.HOST = QLineEdit(self.telnetWindow)  # Creates a Host Line Editor (RM)
        self.HOST.setFixedWidth(200)
        self.HOST.adjustSize()
        self.HOST.move(200, 30)  # Moves it to desire location (RM)
        self.nameTelnet = QLabel("Enter telnet password: ",
                                 self.telnetWindow)  # Creates a Telnetpassword Label (RM) Wednesday night Eureka moment Me and Richard
        self.nameTelnet.adjustSize()
        self.nameTelnet.move(10, 80)  # Moves it to desire location (RM)
        self.telnetPass = QLineEdit(self.telnetWindow)  # Creates a Telnet Line Editor (RM)
        self.telnetPass.setFixedWidth(200)
        self.telnetPass.adjustSize()
        self.telnetPass.move(200, 80)  # Moves it to desire location (RM)
        self.nameEnable = QLabel("Enter enable password: ", self.telnetWindow)  # Creates a Enable password label (RM)
        self.nameEnable.adjustSize()
        self.nameEnable.move(10, 130)  # Moves it to desire location (RM)
        self.enablePass = QLineEdit(self.telnetWindow)  # Creates a Enable Line Editor (RM)
        self.enablePass.setFixedWidth(200)
        self.enablePass.adjustSize()
        self.enablePass.move(200, 130)  # Moves it to desire location (RM)

        self.connectTelnet = QtWidgets.QPushButton("Connect",
                                                   clicked=self.telnetConnection)  # adds push button to connect to device

        self.telnetWindow.layout.addWidget(self.connectTelnet)
        self.telnetWindow.layout.addItem(self.spacer)  # Line add RM to move everything to far left side
        self.telnetWindow.setLayout(self.telnetWindow.layout)

        self.availableDrives = [f'{d}' for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if not os.path.exists(f'{d}:')]
        self.spacer1 = QSpacerItem(100, -300, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.mapFolder.layout = QHBoxLayout(self)
        self.mapFolder.layout.setContentsMargins(0, 160, 0, 0)
        self.driveLetter = QLabel("Enter your preferred drive letter: ", self.mapFolder)
        self.driveLetter.adjustSize()
        self.driveLetter.move(10, 30)
        self.selectedLetter = QComboBox(self.mapFolder)
        self.selectedLetter.addItems(self.availableDrives)
        self.selectedLetter.adjustSize()
        self.selectedLetter.move(200, 30)

        self.path = QLabel("Enter the shared folder full path: ", self.mapFolder)
        self.path.adjustSize()
        self.path.move(10, 80)
        self.enteredPath = QLineEdit(self.mapFolder)
        self.enteredPath.setFixedWidth(200)
        self.enteredPath.setPlaceholderText(" \\\\XXX.XXX.XXX.XXX\\foldername ")
        self.enteredPath.adjustSize()
        self.enteredPath.move(200, 80)

        self.networkUser = QLabel("Enter your FTP host's User name:", self.mapFolder)
        self.networkUser.adjustSize()
        self.networkUser.move(10, 130)
        self.hostUser = QLineEdit(self.mapFolder)
        self.hostUser.setFixedWidth(200)
        self.hostUser.setEchoMode(QtWidgets.QLineEdit.Password)
        self.hostUser.adjustSize()
        self.hostUser.move(200, 130)

        self.networkPass = QLabel("Enter your FTP host's password:", self.mapFolder)
        self.networkPass.adjustSize()
        self.networkPass.move(10, 180)
        self.hostPass = QLineEdit(self.mapFolder)
        self.hostPass.setFixedWidth(200)
        self.hostPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.hostPass.adjustSize()
        self.hostPass.move(200, 180)
        self.mapDrive = QtWidgets.QPushButton("Map a Network Folder",
                                              clicked=self.makingDrive)  # adds push button to connect to device
        self.unmapDrive = QtWidgets.QPushButton("UnMap a Network Folder",
                                                clicked=self.disconnectingDrive)  # adds push button to connect to device
        self.mapFolder.layout.addWidget(self.mapDrive)
        self.mapFolder.layout.addWidget(self.unmapDrive)
        self.mapFolder.layout.addItem(self.spacer1)  # Line add RM to move everything to far left side
        self.mapFolder.setLayout(self.mapFolder.layout)

        self.ftpWindow.layout = QtWidgets.QHBoxLayout(self)
        self.ftpWindow.layout.setContentsMargins(0, 60, 0, 0)
        self.serverAddress = QLabel("Enter your FTP address: ", self.ftpWindow)  # Creates a Hostname Label (RM)
        self.serverAddress.adjustSize()
        self.serverAddress.move(10, 30)  # Moves it to desire location (RM)
        self.address = QLineEdit(self.ftpWindow)  # Creates a Host Line Editor (RM)
        self.address.setFixedWidth(200)
        self.address.move(200, 30)  # Moves it to desire location (RM)
        self.address.adjustSize()
        self.ftpName = QLabel("Enter User name: ",
                              self.ftpWindow)  # Creates a Telnet password Label (RM) Wednesday night Eureka moment Me and Richard
        self.ftpName.move(10, 80)  # Moves it to desire location (RM)
        self.ftpName.adjustSize()
        self.userName = QLineEdit(self.ftpWindow)  # Creates a Telnet Line Editor (RM)
        self.userName.setFixedWidth(200)
        self.userName.move(200, 80)  # Moves it to desire location (RM)
        self.userName.adjustSize()
        self.ftpPass = QLabel("Enter your password: ", self.ftpWindow)  # Creates a Enable password label (RM)
        self.ftpPass.move(10, 130)  # Moves it to desire location (RM)
        self.ftpPass.adjustSize()
        self.userPass = QLineEdit(self.ftpWindow)  # Creates a Enable Line Editor (RM)
        self.userPass.setFixedWidth(200)
        self.userPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.userPass.move(200, 130)  # Moves it to desire location (RM)
        self.userPass.adjustSize()
        self.FTPdownload = QtWidgets.QPushButton("Download From FTP",
                                                 clicked=self.FTPdownload)  # adds push button to connect to device to download
        self.FTPupload = QtWidgets.QPushButton("Upload From FTP",
                                               clicked=self.FTPupload)  # adds push button to connect to device to upload
        self.ftpWindow.layout.addWidget(self.FTPupload)
        self.ftpWindow.layout.addWidget(self.FTPdownload)
        self.ftpWindow.layout.addItem(self.spacer)
        self.ftpWindow.setLayout(self.ftpWindow.layout)

        self.settingsWindow.layout = QtWidgets.QVBoxLayout(self)  # Initializes layout for tab settingWindow
        self.fontSettings = QtWidgets.QPushButton("Fonts",
                                                  clicked=self.userInputFonts)  # Makes a button on settingWindow that sats "Change Font" then runs userInputFonts
        self.settingsWindow.layout.addWidget(self.fontSettings)  # adds btnfontSettings to settingsWindow window
        self.settingsWindow.setLayout(self.settingsWindow.layout)  # sets the layout of settingsWindow window

        self.helpWindow.layout = QtWidgets.QVBoxLayout(self)  # Initialize layout for tab helpWindow
        self.helpPanel = QLabel(self)  # Creates text label

        # Help message to display, just gonna use lorem ipsum for the moment.
        helpPanelMessage = (
            "Lorem Ipsum dolor sit amet, consecteur adipiscing elit, sed do eiusmod tempour incididunt ut labore et dolore magna aliqua.")

        self.helpPanel.setText(helpPanelMessage)  # Sets text of label according to pre-defined var
        self.helpPanel.setAlignment(Qt.AlignLeft)  # Aligns label to the left
        self.helpWindow.layout.addWidget(self.helpPanel)  # Adds help label to helpWindow
        self.helpWindow.setLayout(self.helpWindow.layout)  # sets helpWindow layout.

        self.gradingWindow.layout = QtWidgets.QVBoxLayout()
        #self.gradingWindow.layout = QtWidgets.QGridLayout(self)
        self.masterFile = QtWidgets.QPushButton("Click Here to select a master config", clicked = self.getMasterFile)
        self.gradedFile = QtWidgets.QPushButton("Click Here to select a file to grade", clicked = self.getGradedFile)
        self.grading = QtWidgets.QPushButton("Click Here to grade the file", clicked = self.showGradedFile)

        self.gradingOptions = ["Routing Protocols", "Interfaces", "Telnet", "Static/Default Route(s)"]

        for file in self.gradingOptions:                                                                                                             # checks all the gradingOptions list, and makes checkboxes for each entry
            self.gradeCheckState = QtWidgets.QCheckBox(file, self)
            self.gradeCheckStore.append(self.gradeCheckState)
            self.gradingWindow.layout.addWidget(self.gradeCheckState)


        self.gradingWindow.layout.addWidget(self.masterFile, alignment=QtCore.Qt.AlignLeft)
        self.gradingWindow.layout.addWidget(self.gradedFile, alignment=QtCore.Qt.AlignLeft)
        self.gradingWindow.layout.addWidget(self.grading, alignment=QtCore.Qt.AlignLeft)
        self.gradingWindow.layout.addItem(self.spacer)
        self.gradingWindow.setLayout(self.gradingWindow.layout)


    def fileCheck(self):
        if (path.exists("properties.txt")) == False:                                                                                #Checks to see if the properties.txt file exists
            self.propertiesFile = open("properties.txt", "x")                                                                       #If it doesnt, create the file
            msgBox = QtWidgets.QMessageBox.warning(self, "Welcome", "This seems to be the first time you are opening Quagga \n Would you like to see the tutorial?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No )

            #msgBox = QtWidgets.QMessageBox()
            #msgBox.setIcon(QtWidgets.QMessageBox.Information)                                                                       #Make a popup if the file doesn't exist
            #msgBox.setText("This seems to be the first time you are opening Quagga \n Would you like to see the tutorial?")         #What the popup says
            #msgBox.setWindowTitle("Welcome to Quagga!")                                                                             #Window title of popup
            #msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)                                         #buttons on the popup, eventually these will actually do something

            if msgBox == QtWidgets.QMessageBox.Yes:
                        self.mainTabWidget.setCurrentIndex(7)
                        #print ("hoe")

            #returnValue = msgBox.exec()

    def userInputFonts(self):
        font, ok = QtWidgets.QFontDialog.getFont()                                                                                              # Opens Font dialog, letting user choose fonts and text size etc, then waits for the button "ok" to be pressed

        if ok:                                                                                                                                  # When the "OK" button is pressed, change the fonts of the following widgets MAKE SURE TO AdD ALL NEW WIDGETS TO THIS OR >:(
            self.btnChangeFolder.setFont(font)
            self.btnChangeToCompare.setFont(font)
            self.btnAnotherCompare.setFont(font)
            self.fontSettings.setFont(font)
            self.labelWebsite.setFont(font)
            self.nameHost.setFont(font)
            self.nameTelnet.setFont(font)
            self.nameEnable.setFont(font)


    def readFolder(self):                                                                                                                       # Function that reads what folder the user would like to look in
        try:
            self.TextFiles = []                                                                                                                     # Initialzes the self.Textfiles list
            self.folderChosen = QtWidgets.QFileDialog.getExistingDirectory()                                                                        # Asks the user what folder he wants to use, Opens File Explorer, then assigns the chosen folder to folderChosen
            self.btnChangeFolder.setText(
                self.folderChosen)                                                                                                                  # Changes the text of self.btnChangeFolder to folderChosen(The folder the user chooses)

            for files in os.listdir(
                    self.folderChosen):                                                                                                             # Finds all files in selected directory ending with .txt and adds them to list
                if files.endswith(".txt"):
                    self.TextFiles.append(files)

            if len(self.TextFiles) == 0:                                                                                                           # If the folder the user has chosen does not have any text files, show an error popup asking if theyd like to choose a different folder
                alert = QtWidgets.QMessageBox.warning(self, "Error",
                                                    "Your folder has no files! \n Would you like try again?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Close)
                if alert == QtWidgets.QMessageBox.Yes:
                    self.readFolder()

            self.deleteCheckboxes()                                                                                                                 # Runs deleteCheckboxes function ---- This is needed to clear checkboxes if the user chooses multiple folders
        except FileNotFoundError as error:
            print("Choose another folder")
    def createCheckBoxes(self):  # Function that creates checkboxes for each textfile in the folderChosen

        for file in self.TextFiles:  # for each .txt in the TextFiles list, create a checkbox and add it to the screen
            self.checkBoxState = QtWidgets.QCheckBox(file, self)
            self.checkBoxStore.append(self.checkBoxState)
            self.importWindow.layout.addItem(self.spacer)
            self.importWindow.setContentsMargins(0, 0, 0, 400)
            self.importWindow.layout.addWidget(self.checkBoxState)

    def deleteCheckboxes(
            self):                                                                                                                              # Function that deletes the checkboxes, Otherwise they overlay and blehh --- Runs BEFORE createCheckboxes
        for i in range(len(self.checkBoxStore)):
            if i >= 0:
                i = -1
            self.checkBoxStore[i].deleteLater()                                                                                                 # actually deletes the checkboxes
            self.checkBoxStore.pop()                                                                                                            # removes the instance of the checkbox from the list

        self.createCheckBoxes()                                                                                                                 # Runs createCheckbox Function

    def importToCompare(
            self):  # Changes the focus of the program to the 3rd tab(compareWindow) then runs compareStuff function
        self.removeCompareBoxes()
        self.compare.setCurrentIndex(1)
        self.compareStuff()

    def getMasterFile(self):
        self.masterFileName = QFileDialog.getOpenFileName(self, "Choose a Master File", './')                                                   #button for the user to select the master copy (what is being graded against)
        self.fileNameMaster,throwAway = self.masterFileName                                                                                     #splits how the file is stored so it only shows the path, and not the file type
        masterSplitFilePath = os.path.split(os.path.abspath(self.fileNameMaster))                                                               #splits the file name from the absolute path                               
        self.masterFile.setText("Your master file is: " + self.fileNameMaster)                                                                  #sets button text to file name
        self.file1 = self.fileNameMaster



    def getGradedFile(self):
        self.gradedFileName = QFileDialog.getOpenFileName(self, "Choose a Master File", './')                                                   #button for the user to select the student copy (what is being graded)
        self.fileNameGraded,throwAway = self.gradedFileName                                                                                     #splits how the file is stored so it only shows the path, and not the file type
        gradedSplitFilePath = os.path.split(os.path.abspath(self.fileNameGraded))                                                               #splits the file name from the absolute path 
        self.gradedFile.setText("The file you wish to grade is: " + self.fileNameGraded)                                                        #sets button text to file name
        self.file2 = self.fileNameGraded




    def showGradedFile(self):
        self.removeCompareBoxesGrading()
        totalGradedMark = 0                                                                                                                 #total Mark that the user received
        totalGradeOutOf = 0                                                                                                                 #total mark out of #
        gradedCriteriaOutput = ''
        self.compareStuff()                                                                                                                 #runs compareStuff
        if not self.gradeCriteria:                                                                                                          #checks if any grading checkboxes were selected, if theyre is not, grade the whole file
            totalGradedMark = self.totalLinesA - (len(self.differenceListB))                                                                #gives a total grade by taking all the lines in File A(master) and substracting from the difference list of B(user file)
            totalGradeOutOf = self.totalLinesA                                                                                              #gives out of by taking all the lines in File A(master)
            #print (self.finalGrade)
            gradedCriteriaOutput = "everything"                                                                                             #output for user to know whats graded
        else:
            if "Interfaces" in self.gradeCriteria:                                                                                          #if Interfaces checkbox is selected
                totalGradeOutOf += self.totalInterfaceAppearances                                                                           #totalgrade adds the amount of times interface shows up and all its content
                totalGradedMark += self.totalInterfaceAppearances - self.diffCounterInterfaces                                              #totalgradedmark takes all times interface shows up then subtracts the differences 
                if gradedCriteriaOutput:                                                                                                    #condition to see the gradedCritiaOutput has content, then concats words depending on result so the english is good
                    gradedCriteriaOutput += ", Interfaces"
                else:
                    gradedCriteriaOutput += " Interfaces"
            if "Routing Protocols" in self.gradeCriteria:
                totalGradeOutOf += self.totalRoutingAppearances
                totalGradedMark += self.totalRoutingAppearances - self.diffCounterRouting
                if gradedCriteriaOutput:                                                                                                    #condition to see the gradedCritiaOutput has content, then concats words depending on result so the english is good
                    gradedCriteriaOutput += ", Routing Protocols"
                else:
                    gradedCriteriaOutput += " Routing Protocols"

            if "Static/Default Route(s)" in self.gradeCriteria:
                totalGradeOutOf += self.staticDefaultRouteTotal
                totalGradedMark += self.staticDefaultRouteTotal - self.diffCounterStaticDefault
                if gradedCriteriaOutput:
                    gradedCriteriaOutput += ", Static/Default Route(s)"
                else:
                    gradedCriteriaOutput += " Static/Default Route(s)"
            if "Telnet" in self.gradeCriteria:
                totalGradeOutOf += self.telnetTotal
                totalGradedMark += self.telnetTotal - self.diffCounterTelnet
                if gradedCriteriaOutput:
                    gradedCriteriaOutput += ", Telnet"
                else:
                    gradedCriteriaOutput += " Telnet"

        if totalGradedMark < 0:
            totalGradedMark = 0
        
        self.finalGrade = str(totalGradedMark) + "/" + str(totalGradeOutOf)
        self.showGradedScore = QtWidgets.QLabel("Your Grade for " + gradedCriteriaOutput + " is: " + self.finalGrade)
        self.gradingWindow.layout.addItem(self.spacer)
        self.gradingWindow.setContentsMargins(0,0,0,400)
        self.gradingWindow.layout.addWidget(self.showGradedScore)

    def compareStuff(self):                                                                                                                     #This is where we need to add the comparison shit

        i=0
        z=0
        j=[]
        self.gradeCriteria = []
        if self.folderChosen:
            #print (len(self.TextFiles))
            folderDirectory = self.folderChosen                                                                                                     #Folder where files are stored

            while i < len(self.TextFiles):                                                                                                          #Find which files have been chosen from check boxes
                if self.checkBoxStore[i].isChecked():                                                                                   
                    j.append(i)                                                                                                                     # is a list that stores chosen check boxes location
                i+=1
            self.file1 = folderDirectory + "/" + self.TextFiles[j.pop(0)]                                                                                #create full file location of first file
            self.file2 = folderDirectory + "/" + self.TextFiles[j.pop(0)]   
        else:
            while z < len(self.gradingOptions):
                if self.gradeCheckStore[z].isChecked():
                    add = self.gradingOptions[z]
                    self.gradeCriteria.append(add)
                z+=1
        #print (self.gradeCriteria)

        self.totalLinesA = 0
        self.totalLinesB = 0

        #folderDirectory = self.folderChosen                                                                                                     #Folder where files are stored

        #while i < len(self.TextFiles):                                                                                                          #Find which files have been chosen from check boxes
        #    if self.checkBoxStore[i].isChecked():                                                                                   
        #        j.append(i)                                                                                                                     # is a list that stores chosen check boxes location
        #    i+=1
                       
        #file1 = folderDirectory + "/" + self.TextFiles[j.pop(0)]                                                                                #create full file location of first file
        #file2 = folderDirectory + "/" + self.TextFiles[j.pop(0)]                                                                                #create full file location of first file

        area1 = []                                                                                                                              #List for file 1 interface lines 
        area2 = []
        ospfList = []
        ospfList2 = []
        eigrpList = []
        eigrpList2 = []                                                                                                                                  #List for file 2 interface lines
        extra1 = []                                                                                                                             #List for file 1 extra lines
        extra2 = []                                                                                                                             #List for file 2 extra lines (ip route, hostname)
        telnetListA = []
        telnetListB = []
        #self.file1 = "H:\\Configs&Properties\\C1.txt"
        #self.file2 = "H:\\Configs&Properties\\C2.txt"
        self.staticDefaultRouteTotal = 0                                                                                                        #counts total appearances of static/default routes
        self.telnetTotal = 0                                                                                                                    #counts total appearances of telnet stuff
        self.totalRoutingAppearances = 0                                                                                                        #counts total appearances of routing protocols

        comparisonA = open(self.file1).readlines()
        comparisonB = open(self.file2).readlines()

        ALPHA = string.ascii_letters                                                                                                            #to search for a char as the first item in the list
        count = 0
        triggerCount = False
        telnetTrigger = False
        routingTrigger = False 

        for line in comparisonA:                                                                                                                #For loop to find interface and append lines to area1 nested loop           
            if "!" not in line:    
                self.totalLinesA+=1
            area1.extend([])
            if line.startswith('interface') or line.startswith('router') or line.startswith('line vty'):                                                                                                     #If line starts with interface, create nested list
                triggerCount = True
                area1.append([line])                                                                                                            #Append all lines with " " to nested list
                if line.startswith('line vty'):                                                                                                 #count the amount of telnet appearences
                    if line not in telnetListA:
                        telnetListA.append(line)                                                                                                    #add telnet shit to new list
                    telnetTrigger = True
                    self.telnetTotal+=1
                if line.startswith('router'):                                                                                                   #counts amount of routing protocol appearences
                    self.totalRoutingAppearances+=1  
                    routingTrigger = True         
            if line.startswith(' '):
                area1[count].append(line)                                                                                                       #Append following lines
                if telnetTrigger == True:
                    if line not in telnetListA:
                        telnetListA.append(line)
                    self.telnetTotal+=1
                if routingTrigger == True:
                    self.totalRoutingAppearances+=1
            if line.startswith("!") or line.startswith("line vty 5 15"):
                if triggerCount == True:
                    count += 1                                                                                                           #End when ! is found
                triggerCount = False
                telnetTrigger = False
                routingTrigger = False
                if line.startswith("line vty 5 15"):
                    telnetTrigger = True

                                                                                                                #For loop to find extra lines and append to extra1
            if line.startswith(tuple(ALPHA)):                                                                                                   #If it stars with a Char and is not interface append to extra1
                if line.startswith("interface") or line.startswith('router') or line.startswith('line vty'): 
                    continue
                elif (line not in extra1):
                    extra1.append([(line.strip())])
                    if line.startswith("ip route"):                                                                                             #count total appearences of static/default routes
                        self.staticDefaultRouteTotal+=1 

        count = 0
        triggerCount = False
        telnetTrigger = False 

        for line in comparisonB:                                                                                                                #For loop for file 2 interfaces
            if "!" not in line:
                self.totalLinesB+=1
            area2.extend([])
            if line.startswith('interface') or line.startswith('router') or line.startswith('line vty'):                                       #If line starts with interface, create nested list
                triggerCount = True
                area2.append([line])
                if line.startswith('line vty'):
                    if line not in telnetListB:
                        telnetListB.append(line)    
                    telnetListB.append(line)
                    telnetTrigger = True
            if line.startswith(' '):                                                                                                            #Append all lines with " " to nested list
                area2[count].append(line)
                if telnetTrigger == True:
                    if line not in telnetListB:
                        telnetListB.append(line)    
                    telnetListB.append(line)
            if line.startswith("!") or line.startswith("line vty 5 15"):                                                                                                      #End of appending to nested list
                if triggerCount == True:
                    count += 1
                triggerCount = False
                telnetTrigger = False
                if line.startswith("line vty 5 15"):
                    telnetTrigger = True

        
        self.totalInterfaceAppearances = 0
        i = 0
        if self.gradeCriteria:
            for i in range (len(area1)):
                for x in area1[i]:
                    if "interface" in x:
                        self.totalInterfaceAppearances+=(len(area1[i]))                                                                         #counts total times interface and subinterface stuff shows up
        else:
            pass

        for line2 in comparisonB:                                                                                                               #For loop to find extra lines and append to extra2
            if line2.startswith(tuple(ALPHA)):                                                                                                  #If it stars with a Char and is not interface append to extra2
                if line2.startswith("interface") or line2.startswith('router') or line2.startswith('line vty'):                                                                                               #Skip interfaces
                    continue
                elif (line2 not in extra2):
                    extra2.append([(line2.strip())])

        
        interfaceCount = 0
        area1Innercount = 0
        initialListB = []                                                                                                                    #all interface differences in file 2
        initialListA = []
        differenceListA = []
        self.differenceListB = []
        dummyList = ['cat', 'dog']                                                                                                                    #all interface differences in file 1
        displayListA=[]
        displayListB=[]
        self.diffCounterInterfaces = 0                                                                                                          #stores difference counter of interface stuff
        self.diffCounterRouting = 0                                                                                                             #stores difference counter of routing stuff
        self.diffCounterStaticDefault = 0                                                                                                       #stores difference counter of static/default route stuff
        self.diffCounterTelnet = 0                                                                                                              #stores difference counter of telnet stuff
        linevty04CounterA = 0                                                                                                                   #stores counter for line vty 0 4 shit for file A
        linevty04CounterB = 0                                                                                                                   #stores counter for line vty 0 4 shit for file B
        interfaceList = []
        routingList = []
        routingListB = []
        telnetVTY04ListA = []                                                                                                                   #stores line vty 0 4 shit for file A   
        telnetVTY04ListB = []                                                                                                                   #stores line vty 0 4 shit for file B
        telnetVTY515ListA = []                                                                                                                  #stores line vty 5 15 shit for file A
        telnetVTY515ListB = []                                                                                                                  #stores line vty 5 15 shit for file B        

        if len(area1) > len(area2):
            differenceInterface = len(area1) - len(area2)
            while (differenceInterface > 0):
                #print("monkey2")
                area2.append([dummyList])
                differenceInterface -= 1       
        elif len(area2) > len(area1):
            differenceInterface = len(area2) - len(area1)
            while (differenceInterface > 0):
               # print("monkey")
                area1.append([dummyList])
                differenceInterface -= 1

        num = 0

        for eachInterface in range(0, len(area2)):
            linePresent = False
            if area1[eachInterface] not in area2:
                initialListA.append(area1[eachInterface])
                differenceListA.append(area1[eachInterface])
                displayListA.append((num, 0, len(area1[eachInterface])))
                if (linePresent == False):
                    for innerinterface in range (0, len(area1)):
                        if area1[eachInterface][0] not in area2[innerinterface]:
                            pass
                        else:
                            differenceListA.remove(area1[eachInterface])
                            displayListA.remove((num, 0, len(area1[eachInterface])))
                            linePresent = True
                num+=1
        num=0
        linePresent = False
        for eachInterface in range(0, len(area1)):
            linePresent = False
            if area2[eachInterface] not in area1:
                initialListB.append(area2[eachInterface])
                self.differenceListB.append(area2[eachInterface])
                displayListB.append((num, 0, len(area2[eachInterface])))
                if (linePresent == False):
                    for innerinterface in range (0, len(area1)):
                        if area2[eachInterface][0] not in area1[innerinterface]:
                            pass
                        else:
                            self.differenceListB.remove(area2[eachInterface])
                            displayListB.remove((num, 0, len(area2[eachInterface])))
                            linePresent = True
                num+=1

        for eachInterface in range(0, len(initialListA)):
            for eachOtherInterface in range(0, len(initialListB)):               
                if initialListA[eachInterface][0] in initialListB[eachOtherInterface]:
                    for eachSubInterface in range(1, len(initialListA[eachInterface])):
                        if initialListA[eachInterface][eachSubInterface] not in initialListB[eachOtherInterface]:
                            differenceListA.append(initialListA[eachInterface][eachSubInterface])
                            displayListA.append((eachInterface, eachSubInterface))
                       
                        
        for eachInterface in range(0, len(initialListB)):
            for eachOtherInterface in range(0, len(initialListA)):
                if initialListB[eachInterface][0] in initialListA[eachOtherInterface]:
                    for eachSubInterface in range(1, len(initialListB[eachInterface])):
                        if initialListB[eachInterface][eachSubInterface] not in initialListA[eachOtherInterface]:
                            self.differenceListB.append(initialListB[eachInterface][eachSubInterface])
                            displayListB.append((eachInterface, eachSubInterface))

        for eachInterface in range (0, len(area2)):
            if area2[eachInterface] not in area1:
               for x in area2[eachInterface]:
                    if "interface" in x:                                                                                                    #if "interface" is found in area2, append it to interfaceList
                        interfaceList.append(area2[eachInterface])

        for eachInterface in range (0, len(area2)):
            if area2[eachInterface] not in area1:
               for x in area2[eachInterface]:
                    if "router" in x:                                                                                                       #if "router" is found in area2, append it to routingList
                        routingList.append(area2[eachInterface])
        
        for eachInterface in range (0, len(area1)):
            if area1[eachInterface] not in area2:
               for x in area1[eachInterface]:
                    if "router" in x:                                                                                                       #if "router" is found in area2, append it to routingList
                        routingListB.append(area1[eachInterface])
        
        if "Static/Default Route(s)" in self.gradeCriteria:
            for eachInterface in range (0,len(extra2)):
                if extra2[eachInterface] not in extra1:
                    for x in extra2[eachInterface]:
                        if "ip route" in x:                                                                                                 #if "ip route" is found in area 2, count it
                            self.diffCounterStaticDefault+=1
                            #print (extra2[eachInterface])
        
        telnetTrigger = False
        if "Telnet" in self.gradeCriteria:
                while telnetTrigger == False:
                    for eachInterface in range(0, len(telnetListB)):
                        if telnetListB[eachInterface].startswith("line vty 5 15"):
                            telnetTrigger = True
                            break
                        else:
                            linevty04CounterB+=1
                            telnetVTY04ListB.append(telnetListB[eachInterface])

                telnetTrigger = False
                while telnetTrigger == False:
                    for eachInterface in range(0, len(telnetListA)):
                        if telnetListA[eachInterface].startswith("line vty 5 15"):
                            telnetTrigger = True
                            break
                        else:
                            linevty04CounterA+=1
                            telnetVTY04ListA.append(telnetListA[eachInterface])

                for eachInterface in range (linevty04CounterA, len(telnetListA)):
                    telnetVTY515ListA.append(telnetListA[eachInterface])

                for eachInterface in range (linevty04CounterB, len(telnetListB)):
                    telnetVTY515ListB.append(telnetListB[eachInterface])

                
                for eachInterface in range (0, len(telnetVTY04ListB)):
                    if telnetVTY04ListB[eachInterface] not in telnetVTY04ListA:
                            self.diffCounterTelnet+=1
                            #print (telnetVTY04ListB[eachInterface])

                for eachInterface in range (0, len(telnetVTY515ListB)):
                    if telnetVTY515ListB[eachInterface] not in telnetVTY515ListA:
                            self.diffCounterTelnet+=1
                            #print (telnetVTY515ListB[eachInterface])



        while len(interfaceList) < len(initialListA):                                                                                       #make the interface List the same length as initiallistA
            interfaceList.append("?")

        if "Interfaces" in self.gradeCriteria:                                                                                              #run if the "Interfaces" checkbox is checked           
            for eachInterface in range (0, len(interfaceList)):
                if "?" not in interfaceList[eachInterface]:                                                                                 # IDK WHAT THIS DOES BUT IT BRICKS WITHOUT IT
                    pass
                    if "interface" in initialListB[eachInterface][0] or "interface" in initialListA[eachInterface][0]:                      #look for the word "interface" in the difference lists - needed cause list also has router stuff
                        for eachSubInterface in range(0, len(interfaceList[eachInterface])):
                            if interfaceList[eachInterface][eachSubInterface] not in initialListA[eachInterface]:                           #look if the subinterface stuff is in the initial difference list 
                                self.diffCounterInterfaces+=1                                                                               #if it is, count it
                                #print (interfaceList[eachInterface][eachSubInterface])
                    else:
                        pass
        
        #print (routingList)
        #print (routingListB)
        if "Routing Protocols" in self.gradeCriteria: 
            for eachInterface in range(0, len(routingList)):
                for eachOtherInterface in range (0, len(routingListB)):
                    if routingList[eachInterface][0] in routingListB[eachOtherInterface]:
                        for eachSubInterface in range(1, len(routingList[eachInterface])):
                            if routingList[eachInterface][eachSubInterface] not in routingListB[eachOtherInterface]:
                                #print (routingList[eachInterface][eachSubInterface])
                                #print (routingListB[eachOtherInterface])
                                #print ("------------------")
                                
                                pass
                linePresent = False
                for eachOtherOtherInterface in range(0, len(routingList)):
                    if routingList[eachInterface][0] not in routingListB[eachOtherOtherInterface]:
                        #print (routingList[eachInterface])
                        if (linePresent==False):
                            for innerinterface in range (0, (len(routingListB))):
                                    if routingList[eachInterface][0] not in routingListB[innerinterface]:
                                        continue
                                    else:
                                        #routingList.remove(routingList[eachInterface])
                                        linePresent= True
                                        print ("I AM REMOVED")




        for eachInterface in range(0, len(area2)):
            linePresent = False
            if area1[eachInterface] not in area2:
                initialListA.append(area1[eachInterface])
                differenceListA.append(area1[eachInterface])
                displayListA.append((num, 0, len(area1[eachInterface])))
                if (linePresent == False):
                    for innerinterface in range (0, len(area1)):
                        if area1[eachInterface][0] not in area2[innerinterface]:
                            pass
                        else:
                            differenceListA.remove(area1[eachInterface])
                            displayListA.remove((num, 0, len(area1[eachInterface])))
                            linePresent = True
 

            










            #for eachOtherInterface in range (0, len(routingList)):                                                                                      #run if "Routing Protocols is checked"       
            #   for eachInterface in range (0, len(initialListA)):
            #            if routingList[eachOtherInterface][0] not in initialListA[eachInterface]:
            #                print (initialListA[eachInterface])
            #                self.diffCounterRouting+= (len(routingList[eachOtherInterface]))
            #                print (self.diffCounterRouting)
            #                print (routingList[eachOtherInterface][0])
            #                print ("IMERIUJMBIEBMERJBJUERJB")
            #            else:
            #                for otherInterface in range (0,len(initialListA)):
            #                    if routingList[eachInterface][0] in initialListA[otherInterface]:                                                                          #if the routingList content isnt in the initial difference list
            #                        for insideInterface in range (1, len(routingList[eachInterface])):                                                      #count to the end of this list and increment the thing
            #                            print (routingList[eachInterface][insideInterface])
            #                            if routingList[eachInterface][insideInterface] not in initialListA[otherInterface]:
            #                                self.diffCounterRouting+=1
            #                                print ("ARMADILLO")                                    
            #                                print ("------------------------------------------------------------------------------------------------------------------------")
            #        else:
            #            pass

                        







                        #  print(initialListB[eachInterface][0])
              #  print(initialListA[eachInterface][0])
               # print("------------------------------")
                
                    
                        #print(initialListB[eachInterface][0])
                        #print(initialListB[eachInterface][eachSubInterface])
                        #print()
                       #pass
        displayListA.sort()
        displayListB.sort()
        #print(displayListA)
        #print(displayListB)
        #print(initialListB)
        #print(initialListA)
        #print("-------------------------------------------------------------------")
        #print(self.differenceListB)
        #print("-------------------------------------------------------------------")
        #print("-------------------------------------------------------------------")
        count=0
        extraListA = []                                                                                                                     #List for Extras(not interface) in file 1
        extraListB = []                                                                                                                     #List for Extras(not interface) in file 2
        for eachList in extra1:                                                                                                             #Loop to find differences in extra lists
                if eachList == extra2[count]:
                    count+=1
                elif eachList is not extra2[count]:
                    place=str(extra1[count])
                    place2=str(extra2[count])
                    extraListA.append(place.strip("['']"))                                                                                  #Append difference to extraListA for file A
                    extraListB.append(place2.strip("['']"))                                                                                 #Append difference to extraListB for file B
                    count+=1
        
        self.display = QtWidgets.QListWidget(self)                                                                                               #list widget
        self.display2 = QtWidgets.QListWidget(self)
        
        z=0
        innercount=0
        outercount=0
        count=0
        triggerPrint = False
        triggerExtra = False
        triggerRouter = False
        #print (self.diffCounterRouting)
        #print(extra1)
        #print(extraListA)
        #print(extra2)
        #print(extraListB)
        num=0
        colorNext=0
        colorRouter=0
        #print(self.differenceListB)
        #print(initialListA)
        #for x in range(0, len(displayListA)):
           #print(initialListA[displayListA[x][0]][displayListA[x][1]])

        for z in range(0,len(comparisonA)):                                                                                                 #Add Lists to PYQTList for Display for File A
            a = QListWidgetItem(comparisonA[z]) 
            if num == len(displayListA):                                                                                          #Check for size of differenceList
                triggerPrint=True
            if count == len(extraListA):                                                                                                    #Check for size of extraList
                triggerExtra=True           
            if (triggerPrint == False) and (comparisonA[z]== initialListA[displayListA[num][0]][displayListA[num][1]] and initialListA[displayListA[num][0]][displayListA[num][1]].startswith("router")):
                a.setBackground( QColor('#008000'))
                self.display.addItem(a)
                if displayListA[num][1] == 0:
                    colorRouter = displayListA[num][2]
                num+=1
            elif (triggerPrint == False) and (comparisonA[z]== initialListA[displayListA[num][0]][displayListA[num][1]]):                     #Add color if line is found in interface differenceList 
                if (comparisonA[z-(displayListA[num][1])]) ==  initialListA[displayListA[num][0]][0]:
                    if initialListA[displayListA[num][0]][0].startswith("router"):
                        a.setBackground( QColor('#008000'))
                        self.display.addItem(a)
                    else:
                        a.setBackground( QColor('#E9401C'))
                        self.display.addItem(a)
                        if displayListA[num][1] == 0:
                            colorNext = displayListA[num][2]
                    num+=1
            if colorNext > 0:
                a.setBackground( QColor('#E9401C'))
                self.display.addItem(a)
                colorNext-=1
            if colorRouter > 0:
                a.setBackground( QColor('#008000'))
                self.display.addItem(a)
                colorRouter-=1
            if (triggerExtra == False) and (comparisonA[z].strip() == extraListA[count].strip()):                                           #Add color if line is found is extraList
                #print(comparisonA[z].strip())
                #print(extraListA[count].strip())
                a.setBackground( QColor('#ffff00'))
                self.display.addItem(a)
                count+=1
            self.display.addItem(a)


        z=0
        innercount=0
        outercount=0
        count=0
        triggerPrint = False
        triggerExtra = False
        num=0
        colorNext=0
        colorRouter=0
        for z in range(0,len(comparisonB)):                                                                                                 #Add Lists to PYQTList for Display for File A
            b = QListWidgetItem(comparisonB[z])                    
            if num == len(displayListB):                                                                                          #Check for size of differenceList
                triggerPrint=True
            if count == len(extraListB):                                                                                                    #Check for size of extraList
                triggerExtra=True
            if (triggerPrint == False) and (comparisonB[z]== initialListB[displayListB[num][0]][displayListB[num][1]] and initialListB[displayListB[num][0]][displayListB[num][1]].startswith("router")):                     #Add color if line is found in interface differenceList
                b.setBackground( QColor('#008000'))
                self.display2.addItem(b)
                if displayListB[num][1] == 0:
                    colorRouter = displayListB[num][2]
                num+=1
            elif (triggerPrint == False) and (comparisonB[z]== initialListB[displayListB[num][0]][displayListB[num][1]]):
                if (comparisonB[z-(displayListB[num][1])]) ==  initialListB[displayListB[num][0]][0]:
                    if initialListB[displayListB[num][0]][0].startswith("router"):
                        b.setBackground( QColor('#008000'))
                        self.display2.addItem(b)
                    else:
                        b.setBackground( QColor('#E9401C'))
                        self.display2.addItem(b)
                        if displayListB[num][1] == 0:
                            colorNext = displayListB[num][2]
                    num+=1
            if colorNext > 0:
                b.setBackground( QColor('#E9401C'))
                self.display2.addItem(b)
                colorNext-=1
            if colorRouter > 0:
                b.setBackground( QColor('#008000'))
                self.display2.addItem(b)
                colorRouter-=1
            if (triggerExtra == False) and (comparisonB[z].strip() == extraListB[count].strip()):                                           #Add color if line is found is extraList
                b.setBackground( QColor('#ffff00'))
                self.display2.addItem(b)
                count+=1
            self.display2.addItem(b)
                

        self.compareOutput.layout.addWidget(self.display)
        self.compareOutput.layout.addWidget(self.display2)
    
    def removeCompareBoxes(self):
        try:
            self.compareToImport()
            self.display.deleteLater()
            self.display2.deleteLater()
        except AttributeError as Error:
            print("you got an error")

    def removeCompareBoxesGrading(self):
        try:
            self.display.deleteLater()
            self.display2.deleteLater()
        except AttributeError as Error:
            print("you got an error")

    def compareToImport(self):                                                                                                              # Changes the focus of the program to the 1st(compareWindow)
        self.mainTabWidget.setCurrentIndex(1)

    def telnetConnection(self):
        #try:
            host = self.HOST.text()  # converts Qtextedit-text to readable assign it to a variable
            password1 = self.telnetPass.text()  # converts Qtextedit-text to readable assign it to a variable
            password2 = self.enablePass.text()  # converts Qtextedit-text to readable assign it to a variable

            counter = 0
            try:
                ipaddress.IPv4Address(host)
                counter = 1
            except ValueError:
                counter = 2
            if counter == 1:
                tn = telnetlib.Telnet(host)
                tn.read_until(b"Password: ")  # code reads till device display Password:
                tn.write(password1.encode('ascii') + b"\n")  # now it inputs telnet password
                connectionMsg = QMessageBox()  # assign a variable to a message box
                connectionMsg.setWindowTitle("Connection Information")  # Sets window title of message box
                connectionMsg.setText("Successfully connected to %s" % host)  # sets message in message box
                connectionMsg.setIcon(QMessageBox.Information)  # sets the icon of the message box
                x = connectionMsg.exec_()  # This makes the message box run dont ask me how learnt from youtube. :)
                tn.write(b"enable\n")  # input enable command
                tn.read_until(b"Password: ")  # code reads till device display Password:
                tn.write(password2.encode('ascii') + b"\n")  # now it inputs enable password
                tn.write(b"terminal length 0\n")  # input terminal 0 command (which display output without pause
                tn.write(b"sh run\n")  # input show run command
                time.sleep(5)  # wait for 5 seconds to process and display result of show run
                tn.write(b'exit\n')  # input exit command
                readOutput = tn.read_all()  # read all of the output

                saveOutput1 = QFileDialog.getSaveFileName(self, "Save Your Config At ", "c:\\",
                                                          "Text files (*.txt *.rtf)")  # Open file explorer to make a file to save.
                if '' not in (saveOutput1):  # This is to check if user selected a file to write device's configs.
                    savefile = open(saveOutput1[0],
                                    'w')  # output from getsavefilename only gets filename and file filter this line open filename to write into it.
                    savefile.write(readOutput.decode("utf-8"))  # write the readoutput into new file.
                    savefile.write("\n")
                    savefile.close()  # close the file to save content.
                    saveMsg = QMessageBox()  # assign a variable to a message box
                    saveMsg.setWindowTitle("File Saved")  # Sets window title of message box
                    saveMsg.setText("Successfully saved configs in %s" % saveOutput1[0])  # sets message in message box
                    saveMsg.setIcon(QMessageBox.Information)  # sets the icon of the message box
                    x = saveMsg.exec_()  # This makes the message box run dont ask me how learnt from youtube. :)
                else:
                    nofileMSG = QMessageBox()  # If user didnt select give him error and ask him to select a file .
                    nofileMSG.setWindowTitle("No File select")
                    nofileMSG.setText("Please select a file to save")
                    nofileMSG.setIcon(QMessageBox.Information)
                    n = nofileMSG.exec_()
            else:
                iperrorMSG = QMessageBox()
                iperrorMSG.setWindowTitle("Invalid IP")
                iperrorMSG.setText("Enter valid IP address")
                iperrorMSG.setIcon(QMessageBox.Information)
                y = iperrorMSG.exec_()
        #except TimeoutError as Error:
        #    print("Connection failed, please try again")
        #except ConnectionRefusedError as error:
        #    print("wrong ip, or incorrect username/password")
        #    connectionrefuseMSG = QMessageBox()
        #    connectionrefuseMSG.setWindowTitle("Connection Error")
        #    connectionrefuseMSG.setText("Wrong IP, or Incorrect Username/Password")
        #    connectionrefuseMSG.setIcon(QMessageBox.Information)
        #    n = connectionrefuseMSG.exec_()
    
    def makingDrive(self):
        userName = self.hostUser.text()  # converts Qtextedit-text to readable assign it to a variable
        password = self.hostPass.text()  # converts Qtextedit-text to readable assign it to a variable
        self.driveLetter = self.selectedLetter.currentText()  # converts Qtextedit-text to readable assign it to a variable
        sharePath = self.enteredPath.text()  # converts Qtextedit-text to readable assign it to a variable

        os.system('net use ' + self.driveLetter + ': ' + sharePath + ' /user:' + userName + ' ' + password)  # command to connect to network drive
        mapMsg = QMessageBox()
        mapMsg.setWindowTitle("Information")
        if (os.path.exists(self.driveLetter + ':')):  # This is to check if network drive is mapped if not asks user to verify his information.
            mapMsg.setText("Folder has been successfully mapped %s" % self.driveLetter + ":" + sharePath)
            mapMsg.exec_()
        else:
            mapMsg.setText("Error mapping driver, please verify your information")
            mapMsg.setIcon(QMessageBox.Information)
            mapMsg.exec_()

    def disconnectingDrive(self):  # This is to unmap network drive as per user desire.
        unmapMsg = QMessageBox()
        unmapMsg.setWindowTitle("Warning")
        unmapMsg.setText("Would you like to unmap network drive? ")
        unmapMsg.setIcon(QMessageBox.Warning)
        unmapMsg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        unmapButton = unmapMsg.exec()

        if unmapButton == QMessageBox.Yes:
            os.system('net use ' + self.driveLetter + ': ' + '/delete')
            unmappedMsg = QMessageBox()
            unmappedMsg.setWindowTitle("Information")
            unmappedMsg.setText("You have successfully unmapped your network drive")
            unmappedMsg.setIcon(QMessageBox.Information)
            unmappedMsg.exec_()

    def FTPdownload(self):
        try:
            ftpAddress = self.address.text()  # converts Qtextedit-text to readable assign it to a variable
            ftpUser = self.userName.text()  # converts Qtextedit-text to readable assign it to a variable
            ftpPassword = self.userPass.text()  # converts Qtextedit-text to readable assign it to a variable

            self.ftp = ftplib.FTP(ftpAddress)  # Connects to a ftp folder.
            self.ftp.login(user=ftpUser, passwd=ftpPassword)  # FTP login
            self.ftp.set_pasv(False)  # makes FTP connection Active.

            connectionMsg = QMessageBox()  # assign a variable to a message box
            connectionMsg.setWindowTitle(self.ftp.getwelcome())  # Sets window title of message box
            connectionMsg.setText("Successfully connected to %s" % ftpAddress)  # sets message in message box
            connectionMsg.setIcon(QMessageBox.Information)  # sets the icon of the message box
            connectionMsg.setInformativeText("Would you like to continue? ")  # asks user if they would like to continue
            connectionMsg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)  # 2 buttons options yes or no

            downButton = connectionMsg.exec()  # This makes the message box run don't ask me how learnt from youtube. :)

            if downButton == QMessageBox.Yes:  # if yes is pressed do following

                downloadSelect = QFileDialog.getOpenFileName(self, "Select the file to download ",
                                                             "\\\\" + ftpAddress + "\\ProjectFTP",
                                                             "Text files (*.txt)")  # after mapping a shared folder this will open filedialog to mapped folder
                downloadRead = open(downloadSelect[0]).read()  # To read  contents of selected download file.

                downloadLocation = QFileDialog.getSaveFileName(self, "Where you would like to save your download? ",
                                                               "c:\\",
                                                               "Text files (*.txt)")  # asks user to pick a file to download from FTP
                saveFile = open(downloadLocation[0], 'w+')  # To open save file to write download file contents
                saveFile.write(downloadRead)  # To write in save file the contents of download file
                saveFile.close()  # To close save file.
                downloadMsg = QMessageBox()  # assigns a variable to messagebox
                downloadMsg.setWindowTitle("Information")  # messagebox title
                downloadMsg.setText("File has been successfully downloaded at %s" % downloadLocation[0])  # gives information to user that file has been downloaded
                downloadMsg.exec_()  # this is to run message got this from youtube.

            elif downButton == QMessageBox.No:  # if no is pressed do following
                self.ftp.close()  # close close FTP
                self.disConectMsg = QMessageBox()  # assigns a variable to messagebox
                self.disConectMsg.setWindowTitle(self.ftp.close())  # show FTP server closing message as window title
                self.disConectMsg.setText(
                    "Successfully disconnected to %s" % ftpAddress)  # display disconnection message
                self.disConectMsg.exec_()  # this is to run message got this from youtube.
        except TimeoutError as error:
            print(
                "A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond")
        except AttributeError as error:

            incorrectInfo = QMessageBox()
            incorrectInfo.setWindowTitle("Information")
            incorrectInfo.setText("Username or Password Incorrect")
            incorrectInfo.setIcon(QMessageBox.Information)
            incorrectInfo.exec_()

    def FTPupload(self):
        try:
            ftpAddress = self.address.text()  # converts Qtextedit-text to readable assign it to a variable
            ftpUser = self.userName.text()  # converts Qtextedit-text to readable assign it to a variable
            ftpPassword = self.userPass.text()  # converts Qtextedit-text to readable assign it to a variable

            self.ftp = ftplib.FTP(ftpAddress)  # Connects to a ftp folder.
            self.ftp.login(user=ftpUser, passwd=ftpPassword)  # FTP login
            self.ftp.set_pasv(False)  # makes FTP connection Active.

            connectionMsg = QMessageBox()  # assign a variable to a message box
            connectionMsg.setWindowTitle(self.ftp.getwelcome())  # Sets window title of message box
            connectionMsg.setText("Successfully connected to %s" % ftpAddress)  # sets message in message box
            connectionMsg.setIcon(QMessageBox.Information)  # sets the icon of the message box
            connectionMsg.setInformativeText("Would you like to continue? ")  # asks user if they would like to continue
            connectionMsg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)  # 2 buttons options yes or no

            downButton = connectionMsg.exec()  # This makes the message box run don't ask me how learnt from youtube. :)

            if downButton == QMessageBox.Yes:  # If yes is pressed do following

                uploadSelect = QFileDialog.getOpenFileName(self, "Select the file to upload ", "c:\\",
                                                           "Text files (*.txt)")  # asks user to select their to upload.
                uploadRead = open(uploadSelect[0]).read()  # open and read the contents of the file.
                uploadLocation = QFileDialog.getSaveFileName(self, "Select where you would like to upload",
                                                             "\\\\" + ftpAddress + "\\ProjectFTP",
                                                             "Text files (*.txt)")  # asks user to pick a file to download from FTP
                saveFile = open(uploadLocation[0], 'w+')  # open a file for upload
                saveFile.write(uploadRead)  # write contents into upload file from user file.
                saveFile.close()  # close upload file.
                uploadMsg = QMessageBox()  # assign a variable to a message box
                uploadMsg.setWindowTitle("Information")  # messagebox title
                uploadMsg.setText("File has been successfully uploaded at %s" % uploadLocation[0])  # gives information to user that file has been uploaded
                uploadMsg.exec_()  # this is to run message got this from youtube.

            elif downButton == QMessageBox.No:  # If no is pressed do following
                self.ftp.close()  # close close FTP
                disConectMsg = QMessageBox()  # assigns a variable to messagebox
                disConectMsg.setWindowTitle(self.ftp.close())  # show FTP server closing message as window title
                disConectMsg.setText("Successfully disconnected to %s" % ftpAddress)  # display disconnection message
                disConectMsg.exec_()  # this is to run message got this from youtube.
        except TimeoutError as error:
            print(
                "A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond")
        except AttributeError as error:
            incorrectInfo = QMessageBox()
            incorrectInfo.setWindowTitle("Information")
            incorrectInfo.setText("Username or Password Incorrect")
            incorrectInfo.setIcon(QMessageBox.Information)
            incorrectInfo.exec_()

    def closeEvent(self, event):   # This will be called when app is been closed
        try:
            if (os.path.exists(self.driveLetter + ':')):  # this will unmap network drive if user forgot to unmap it before closing
                os.system('net use ' + self.driveLetter + ': ' + '/delete')
        except:
            pass

width = 1200
height = 800

if __name__ == "__main__":                                                                                                                  # I Have no idea what this actually does, but everyone else has it and im a sheep

    app = QtWidgets.QApplication(sys.argv)                                                                                                  # Makes the program an app? I honest dont know either
    #screen_rect = app.desktop().screenGeometry()                                                                                          #Finds your current screen resolution
    #width, height = screen_rect.width(), screen_rect.height()                                                                             #Sets width and height to your monitor resolution
    w = allTheThings()                                                                                                                      # makes w  = the class allTheThings
    w.resize(width, height)                                                                                                                 # Sets default screensize
    w.show()  
    w.fileCheck()                                                                                                                              # Show the class allTheThings to the screens
    sys.exit(app.exec_())
