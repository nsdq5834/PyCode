# CopyQB.py
# Version 1.1

# This is a simple utility program to backup specific files, in this case we
# are backing up our Quicken database. The backup copies are going to be 
# encrypted.

# Copy in needed support code

from os import *
from io import open
from shutil import copy2
from filecmp import dircmp
from datetime import datetime
#from pyAesCrypt import encryptFile

# Define and initialize some variables we will use.

sourceFile = ''
targetFile = ''
QbSflag = False
QbTflag = False
QbPflag = False
QbLflag = False
SDfiles = []
TDfiles = []
kByte = 1024
bufferSize = 64 * kByte

# See if we can open the parameter file.

try:
    parmFile = open("CopyQB.parms","r",1)
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
  
  if myLines[0].strip() == "QbSrc" :
    QbSpath = myLines[1].strip()
    QbSflag = True
	
  if myLines[0].strip() == "QbTgt" :
    QbTpath = myLines[1].strip()
    QbTflag = True

  if myLines[0].strip() == "QbLfl" :
    QbLogFileLoc = myLines[1].strip()
    QbLflag = True	
  
parmFile.close()

# Trivial test to make sure we have the three parameters we need.

if (QbSflag == False or QbTflag == False or QbLflag == False) :
  print('Parameter error in a parm file record.')
  exit()
  
# Next we need to construct a log file name and then open it for output.
# Grab the current date and time

rightNow = datetime.now()
logFile = QbLogFileLoc + "CopyQB_" + rightNow.strftime("%Y%m%d_%H%M%S") + ".log"

logHandle = open(logFile,"w+")

# Check to make sure the directories exist.

if not path.isdir(QbSpath) :
  errMsg = QbSpath + ' is not a directory, exiting routine\n'
  logHandle.write(errMsg)
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