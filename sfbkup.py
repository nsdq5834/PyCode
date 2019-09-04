# sfbkup.py
# Version 1.0

# Python program to create backups of files. The list of files to be backed
# is specified in the sfbkup.parms file. This file contains a list of direc-
# tories that will be scanned to build a list of the files that need to be
# backed up.

# Copy in needed support code

from os import *
from io import open
from shutil import copy2
from filecmp import dircmp
from datetime import datetime

# open_the_logfile is a simple function that accepts two parameters and uses
# them to create a unique name for a log file, and then opens the file. If we 
# are able to open the file, the file descriptor or handle is passed back.
# If we encounter an error we will exit the routine.

def open_the_logfile(otl_tuple) :

  localList = list(otl_tuple)	
  LogFileLocation = localList[0]
  LogFileNamePrefix = localList[1]  
  
  rightNow = datetime.now()
  logFile = LogFileLocation + LogFileNamePrefix + rightNow.strftime("%Y%m%d_%H%M%S") + ".log"
  
  try:
    LogFileDescriptor = open(logFile,"w+")
  except PermissionError:
    print('Access permission error')
    exit()
  except OSerror:
    print('OS error encountered')
    exit()
  else:
    return LogFileDescriptor

def write_to_logfile(wtl_tuple) :

    fileDescriptor = wtl_tuple[0]
    messageText = wtl_tuple[1]
    rightNow = datetime.now()
    timeStamp = rightNow.strftime("%Y%m%d_%H%M%S")
    logMessage = timeStamp + ' ' + messageText
    fileDescriptor.write(logMessage)

    return True	

# Define and initialize some variables we will use.

sourceFile = ''
targetFile = ''
logHandle = ''
QbSflag = False
QbLflag = False
sourceDirect = []
targetDirect = []
sourceFiles = []
targetFiles = []

# See if we can open the parameter file.

try:
    parmFile = open("sfbkup.parms","r",1)
except PermissionError:
    print('Access permission error')
    exit()
except FileNotFoundError:
    print('File does not exist or not found')
    exit()
else:
    isReadable = parmFile.readable()

# Read and process the parameter file. Very simple logic to isolate the
# parameters we need.

for lines in parmFile:

  myLines = lines.split("=",2)
  
  if myLines[0].strip() == "BkSrc" :
    QbSpath = myLines[1].strip()
    QbSflag = True

  if myLines[0].strip() == "BkLfl" :
    QbLogFileLoc = myLines[1].strip()
    QbLflag = True	
  
parmFile.close()

# Trivial test to make sure we have the two parameters we need.

if (QbSflag == False or QbLflag == False) :
  print('Parameter error in a parm file record.')
  exit()
  
# We have the location for the log file, so we will try to create it.
# We will create a simple tuple to pass to the open_the_logfile routine.
# If we have a log file go ahead and write a couple of messages to it.

myTuple = (QbLogFileLoc, "sfbkup_")
logHandle = open_the_logfile(myTuple)

myTuple = (logHandle, 'Beginning program execution.\n')
QbLflag = write_to_logfile(myTuple)
myTuple = (logHandle, 'Processing records from source file.\n')
QbLflag = write_to_logfile(myTuple)
 
"""
try:
    BkSrc = open(QbSpath,"r",1)
except PermissionError:
    print('Access permission error')
    exit()
except FileNotFoundError:
    print('File does not exist or not found')
    exit()
else:
    isReadable = BkSrc.readable()
	
for lines in BkSrc :
  sourceDirect.append(lines.strip())
  
BkSrc.close()

# At this point sourceDirect contains the base list of directories that we will
# examine for backup opportunities.

for SD in sourceDirect :
  xyz = scandir(SD)
  for abc in xyz :
    print(abc)
"""

if not path.isdir(QbSpath) :
  errMsg = QbSpath + ' is not a directory, exiting routine\n'
  myTuple = (logHandle, errMsg)
  QbLflag = write_to_logfile(myTuple)
  exit()
else :
  txtMsg = 'Source directory is ' + QbSpath + '\n'
  logHandle.write(txtMsg)
  
if not path.isdir(QbTpath) :
  errMsg = QbTpath + ' is not a directory, exiting routine\n'
  logHandle.write(errMsg)
  exit()
else :
  txtMsg = 'Target directory is ' + QbTpath + '\n'
  logHandle.write(txtMsg)
  
txtMsg = 'Source and target directories are valid\n'
logHandle.write(txtMsg)

txtMsg = 'Obtaining list of files in source and not in target\n'
logHandle.write(txtMsg)

# We are going to use the dircmp function from filecmp. This will do a
# comparison of the source and target directories. From that we will use
# the left_only property to obtain a list of files that are in the source
# directory, but not in the target directory.

filesNeedingBackup = dircmp(QbSpath,QbTpath,None,None).left_only

# Now that we have the list of files we can iterate over them and back them
# up using the copy2 method.

for FNB in filesNeedingBackup :
  sourceFile = QbSpath + FNB
  targetFile = QbTpath + FNB
  try:
    copy2(sourceFile, targetFile)
  except OSError:
    print("Error")
  else:
    txtMsg = sourceFile + ' has been copied to target directory\n'
    logHandle.write(txtMsg)

logHandle.write('Exiting program\n')  
logHandle.close()

exit()