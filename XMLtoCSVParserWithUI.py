# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 09:38:06 2019

@author: Karonjot.singh

"""
import xml.etree.ElementTree as XML
dataSetList = []
import tkinter as tk
from tkinter import filedialog
import os
import csv



###############################################################################
"""
User input section
"""
#two Global Variables to get the file to read and file to write
c=""
d= ""

# variable to get network name as default
e= None
# Specify the path to the xml settings file you want to read
#Function to select FileToRead and Define title for tkinter Window
def clicked(event=None):
    my_filetype = [ ('xml files', '.xml')]
    fileToRead = filedialog.askopenfilename(parent=application_window,
                                     initialdir=os.getcwd(),
                                     title="Please select a file:",
                                     filetypes=my_filetype)
    
    
    
    
################## SPECIAL SECTION ############################################
    #To save CSV file as your default NetworkName in Settings.xml File
    path= ''.join(fileToRead)
    fileToRead=path.replace('\\','\\\\')
    tree = XML.parse(fileToRead)
    root = tree.getroot()
    # Data section
    for DataSet in root.iter("Dataset"):
        rowToWrite = []
            # grab all the data for a row and put it in a list
        datasetName = DataSet.get("Name")
        rowToWrite.append(datasetName)
        for ValidationPiece in DataSet.iter("ValidationPiece"):
            pieceNumber = ValidationPiece.get("Piece")
            rowToWrite.append(pieceNumber)
            for Surfaces in ValidationPiece:
                surface = (Surfaces.tag)
                rowToWrite.append(surface)
                for Networks in Surfaces:
                    network = Networks.get("NetworkName")
     
    global e
    e.set(network)     
###############################################################################      




    PathforFileToRead = tk.Label(mainWindowframe, text=str(fileToRead))
    PathforFileToRead.place(x=70,y=35)
    makeFilesPathGlobal(fileToRead, nameOutputCSV)

#Function to make file Path Global
def makeFilesPathGlobal(getFileToRead, nameOutputCSV):
     global c
     global d
     c = getFileToRead
     d= nameOutputCSV


def RunMainwindow(event=None):
    global c
    global d
    global networkName
    main(c, str(d.get()))
    application_window.destroy()
    


def main(fileToRead, fileToWrite):

    path= ''.join(fileToRead)
    fileToRead=path.replace('\\','\\\\')
    tree = XML.parse(fileToRead)
    root = tree.getroot()
    print(fileToWrite)

# Specify the path where you want to save the CSV file
    
    pathforCSV= fileToRead.strip('Settings.xml') + fileToWrite +".csv"
    path=''.join(pathforCSV)
    
    # Set your metric bounds
    iouBound            = float(IOUtype.get())    # Decimal value
    precBound           = float(Precisiontype.get())    # Decimal value
    recBound            = float(RecallType.get())     # Decimal value
    falseposBound       = float(FP_pixelsType.get())    # Pixel Threshold
    groundtruthBound    = float(GT_pixelsType.get())    # Pixel Threshold
    orPixBound          = float(OrPixels.get())    # Pixel Threshold 
    

    ##########################################################################
    """
    Don't touch unless you know what's good for you section
    """
    ###########################################################################
    # parse xml to tree and get root

    # file to write to
    data = open(pathforCSV, 'w')

    # csv writer objects
    csvwriter = csv.writer(data, delimiter=',', lineterminator='\n')
    csvHeaderWriter = csv.DictWriter(data,
                                     fieldnames=["DataSet", "Piece", "Surface",
                                                 "Network", "Defect", "IOU",
                                                 "Precision", "Recall", "OrPix",
                                                 "FalsePositivePix",
                                                 "GroundTruthPix"],
                                                 lineterminator="\n")



    # Header section
    csvHeaderWriter.writeheader()

    # Data section
    for DataSet in root.iter("Dataset"):
        rowToWrite = []
        # grab all the data for a row and put it in a list
        datasetName = DataSet.get("Name")
        rowToWrite.append(datasetName)
        for ValidationPiece in DataSet.iter("ValidationPiece"):
            pieceNumber = ValidationPiece.get("Piece")
            rowToWrite.append(pieceNumber)
            for Surfaces in ValidationPiece:
                surface = (Surfaces.tag)
                rowToWrite.append(surface)
                for Networks in Surfaces:
                    network = Networks.get("NetworkName")
                    defect = Networks.get("DefectName")
                    iou = Networks.get("IOU")
                    prec = Networks.get("Precision")
                    rec = Networks.get("Recall")
                    orPix = Networks.get("ImageOrPixels")
                    falsepos = Networks.get("FalsePositivePixels")
                    groundtruth = Networks.get("GroundTruthPixels")

                    rowToWrite.append(network)
                    rowToWrite.append(defect)
                    rowToWrite.append(iou)
                    rowToWrite.append(prec)
                    rowToWrite.append(rec)
                    rowToWrite.append(orPix)
                    rowToWrite.append(falsepos)
                    rowToWrite.append(groundtruth)

                    # Three cases: GT has value, FP has value, or stats have value
                    if(groundtruth != None):
                        if(float(groundtruth) >= float(groundtruthBound)):
                            csvwriter.writerow(rowToWrite)
                    elif(falsepos != None):
                        if(float(falsepos) >= float(falseposBound)):
                            csvwriter.writerow(rowToWrite)
                    elif(orPix != None):
                        if(float(orPix) >= float(orPixBound)):
                            csvwriter.writerow(rowToWrite)
                    elif(float(iou) <= float(iouBound) and
                    float(prec) <= float(precBound) and
                    float(rec) <= float(recBound)):
                        csvwriter.writerow(rowToWrite)

                    # Pop everything off the list to create new row
                    while(len(rowToWrite) > 3):
                        rowToWrite.pop()
                rowToWrite.pop()
            rowToWrite.pop()
        rowToWrite.pop()

    data.close()


#Geometry For Tkinter Window
application_window = tk.Tk()
application_window.title("File selection")
application_window.geometry('600x400')

#Application Window frame
mainWindowframe= tk.Frame(application_window)
mainWindowframe.pack(fill='both', expand='yes')

LabelforFileToRead = tk.Label(mainWindowframe, text="Find the Settings.xml file you want to parse")
LabelforFileToRead.place(x=10,y=10)




#Label to get IOU value in Application Window
GetIOU = tk.Label(mainWindowframe, text="IOU:")
GetIOU.place(x=10,y=125)
IOUtype = tk.StringVar()
IOUgeometry = tk.Entry(mainWindowframe, width=6, textvariable=IOUtype)
IOUtype.set('0.9')
IOUgeometry.place(x=70, y=125)

#Label to get PRECISION value in Application Window
GetPrecision = tk.Label(mainWindowframe, text="Precision:")
GetPrecision.place(x=10,y=150)
Precisiontype = tk.StringVar()
PrecisionGeometry = tk.Entry(mainWindowframe, width=6, textvariable=Precisiontype)
Precisiontype.set('0.9')
PrecisionGeometry.place(x=70, y=150)

#Label to get REcall value in Application window
GetRecall = tk.Label(mainWindowframe, text="RECALL:")
GetRecall.place(x=10,y=175)
RecallType = tk.StringVar()
RecallGeometry = tk.Entry(mainWindowframe, width=6, textvariable=RecallType)
RecallType.set('0.9')
RecallGeometry.place(x=70, y=175)

#Label to get FalsePositivePIxel in Application Window
GetFP_pixels = tk.Label(mainWindowframe, text="FalsePositive_Pixels:")
GetFP_pixels.place(x=10,y=230)
FP_pixelsType = tk.StringVar()
FPPGeometry = tk.Entry(mainWindowframe, width=6, textvariable=FP_pixelsType)
FP_pixelsType.set('0')
FPPGeometry.place(x=130, y=230)


#Label to get GroundTruth_Pixels in Application Window
GetGroundTruth_pixels = tk.Label(mainWindowframe, text="GroundTruth_Pixels:")
GetGroundTruth_pixels.place(x=10,y=255)
GT_pixelsType = tk.StringVar()
GTPgeometry = tk.Entry(mainWindowframe, width=6, textvariable=GT_pixelsType)
GT_pixelsType.set('0')
GTPgeometry.place(x=130, y=255)


#Label to get ORPIXELs in Application Window
GetOR_pixels = tk.Label(mainWindowframe, text="OR_Pixels:")
GetOR_pixels.place(x=10,y=280)
OrPixels = tk.StringVar()
ORPgeometry = tk.Entry(mainWindowframe, width=6, textvariable=OrPixels)
OrPixels.set('0')
ORPgeometry.place(x=130, y=280)



#Button to find the xml file which is fileToRead
FIND_XML_btn = tk.Button(application_window,text="Find", command=clicked)
FIND_XML_btn.pack(side="right", fill='both', padx=20, pady=20)
FIND_XML_btn.place(x = 250, y = 10)

#Label to name the CSV File
SaveOutputCSV=tk.Label(mainWindowframe, text="Save your file as:")
SaveOutputCSV.place(x=50,y=320)

#Save your file to Write as you want
nameOutputCSV = tk.StringVar()
nameEntered = tk.Entry(mainWindowframe, width=40, textvariable=nameOutputCSV)
e = nameOutputCSV
nameEntered.place(x=155, y=320)

#Click Button RUN to get your output CSV File where the Setting.xml  file is stored
RUN_MainWindow_btn = tk.Button(application_window,text="RUN", command=RunMainwindow)
RUN_MainWindow_btn.pack(side="right", fill='both', padx=4, pady=4)
RUN_MainWindow_btn.place(x = 500, y = 360)

application_window.mainloop()







###############################################################################
