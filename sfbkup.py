# sfbkup.py
# Version 1.00
# Version 1.01
# Version 1.02

# Python program to create backups of files. The list of files to be backed
# is specified in the sfbkup.parms file. This file contains a list of direc-
# tories that will be scanned to build a list of the files that need to be
# backed up.

# Copy in needed support code

from os import *
from sys import setrecursionlimit
from subprocess import call
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

#
# write_to_logfile is a simple routine to allow us to write standardized mes-
# sages to a logging file.
#

def write_to_logfile(wtl_tuple) :

    fileDescriptor = wtl_tuple[0]
    messageText = wtl_tuple[1]
    rightNow = datetime.now()
    timeStamp = rightNow.strftime("%Y%m%d_%H%M%S")
    logMessage = timeStamp + ' ' + messageText
    fileDescriptor.write(logMessage)

    return True

# enum_directory is a simple funtion that is used to locate and save
# directory entries.
#
# We call the routine with a tuple that contains two entries. The first entry
# is the list of the source directories that we are building. The second entry
# is the current entry we are examining.
#
# We use the try/except/else logic block to catch any errors that may occur.
# We should never encounter the NotADirectoryError, but it is used as a safety.
# We are more likely to encounter the PermissionError as we may be executing
# the script as a normal user and not and administrator.
#
# There is most likely a more elegant way to obtain the list of directories and
# subdirectories, but I have started with this method as I am trying to learn
# Python.
#
# Note that were calling the routine recusively.
    
def enum_directory(ed_tuple) :

    localList = list(ed_tuple)
    sdList = localList[0]
    currentDirect = localList[1]
    
    try :
      localDirectory = scandir(currentDirect)
    except NotADirectoryError :
      return False
    except PermissionError :
      return False
    else :
      sdList.append(currentDirect)
      for localEntry in localDirectory :
        if localEntry.is_dir():         
          localTuple = (sdList, localEntry.path)
          localFlag = enum_directory(localTuple)
          
      return True

# Set our recursion limit/depth.

setrecursionlimit(10000)

# Define and initialize some variables we will use.

sourceFile = ''
targetFile = ''
logHandle = ''
backupPrefix = 'D:\Asus SyncFolder\@BU\\'

QbEflag = False
QbSflag = False
QbLflag = False
EnumFlag = False

baseDirect = []
baseExcept = []
sourceDirect = []
targetDirect = []
sourceFiles = []
targetFiles = []

sourceFile = []
sourcePath = []
sourceMtime = []
sourceSize = []

targetFile = []
targetPath = []
targetMtime = []
targetSize = []

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

  if myLines[0].strip() == "BkExc" :
    QbEpath = myLines[1].strip()
    QbEflag = True

  if myLines[0].strip() == "BkLfl" :
    QbLogFileLoc = myLines[1].strip()
    QbLflag = True  
  
parmFile.close()

# Trivial test to make sure we have the two parameters we need.

if (QbEflag == False or QbSflag == False or QbLflag == False) :
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

#
# Next we will process the source directory file. This file contains the base
# set of directories we will start with. If we are able to open the file then
# we will read the files contents, and then close the file.
# 

linesRead = 0
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
  baseDirect.append(lines.strip())
  linesRead += 1
  
BkSrc.close()

logMessage = 'Number of base directories = ' + str(linesRead) +'\n'
myTuple = (logHandle, logMessage)
QbLflag = write_to_logfile(myTuple)

#
# Next we will process the exclusion list file. These are known directories
# that we do not want to attempt to backup. If we are able to open the
# file, we will read the file contents and then close the file.
#

linesRead = 0
try:
    BkExc = open(QbEpath,"r",1)
except PermissionError:
    print('Access permission error')
    exit()
except FileNotFoundError:
    print('File does not exist or not found')
    exit()
else:
    isReadable = BkExc.readable()
    
for lines in BkExc :
  baseExcept.append(lines.strip())
  linesRead += 1
  
BkExc.close()

logMessage = 'Number of directories to exclude = ' + str(linesRead) +'\n'
myTuple = (logHandle, logMessage)
QbLflag = write_to_logfile(myTuple)

# At this point sourceDirect contains the base list of directories that we will
# examine for backup opportunities. This will be our main loop for building the
# complete list of directories we will back up.
#
# We are going to use a tuple to call the enum_directory function. We will re-
# turn a boolean flag.

for SD in baseDirect :
    myTuple = (sourceDirect, SD)
    EnumFlag = enum_directory(myTuple)
    
#
# Now that we have the total list of directories that are to be backed up,
# we will remove any direcory that was in the exclude list.
#

for ED in baseExcept :
    try :
      sourceDirect.remove(ED)
    except ValueError :
      pass

#
# At this point we have located all of the source directories that we will pro-
# cess. We sort the list of directories. Next we create the matching list of
# target directories that we will back files up to.
#

logMessage = 'Total number of directories to process = ' + str(len(sourceDirect)) +'\n'
myTuple = (logHandle, logMessage)
QbLflag = write_to_logfile(myTuple)

sourceDirect.sort()

myTuple = (logHandle, 'Source directory list has been sorted.\n')
QbLflag = write_to_logfile(myTuple)


# Now create the list of target directories.

sourceTotal = 0

for SD in sourceDirect :
    splitSD = SD.split('\\', 1)
    BD = backupPrefix + splitSD[1]
    targetDirect.append(BD)
    sourceTotal += 1  

targetTotal = sourceTotal
  
myTuple = (logHandle, 'Target directory list has been built.\n')
QbLflag = write_to_logfile(myTuple)
myTuple = (logHandle, 'Checking for the existence of target directories.\n')
QbLflag = write_to_logfile(myTuple)

#
# Next we will iterate through the list of target directories directories to
# make sure they all exist. If we get a FileNotFoundError we will go ahead and
# create the target directory.
#

for TD in targetDirect :
#    print(TD, '\n')
    try :
      scandir(TD)
    except FileNotFoundError :
      mkdir(TD)
      logMessage = 'Directory created = ' + TD +'\n'
      myTuple = (logHandle, logMessage)
      QbLflag = write_to_logfile(myTuple)

myTuple = (logHandle, 'Completed checking for target directories.\n')
QbLflag = write_to_logfile(myTuple)

#
# The following is the main loop for determining if an individual file needs
# to be backed up. We do this by going through all of the source and matching
# target directories looking for files that are on the source and not on the
# target, or files on the source and target with the same name but different
# date/time stamps and/or file size.
#

sourcePointer = 0
totalFilesBackedUp = 0
totalBytes = 0

for sourcePointer in range(sourceTotal) :

    sdFlag = False
    try:
      sourceEntries = scandir(sourceDirect[sourcePointer])
    except NotADirectoryError :
      pass
    except PermissionError :
      pass
    else :
      sdFlag = True
      seCounter = 0
      for SE in sourceEntries :
        if SE.is_file() :
          sourceFile.append(SE.name)
          sourcePath.append(SE.path)
          statVals = SE.stat()
          sourceMtime.append(statVals.st_mtime)
          sourceSize.append(statVals.st_size)
          sdFlag = True
          seCounter += 1

    if sdFlag : 
      tdFlag = False
      try:
        targetEntries = scandir(targetDirect[sourcePointer])
      except NotADirectoryError :
        pass
      except PermissionError :
        pass
      else :
        tdFlag = True
        for TE in targetEntries :
          if TE.is_file() :
            targetFile.append(TE.name)
            targetPath.append(TE.path)
            statVals = TE.stat()
            targetMtime.append(statVals.st_mtime)
            targetSize.append(statVals.st_size)
      
      if sdFlag and tdFlag :
        for sfPointer in range(seCounter) :
          try :
            tfPointer = targetFile.index(sourceFile[sfPointer])
          except ValueError :
            sourceFileEntry = sourcePath[sfPointer]
            splitSD = sourceFileEntry.split('\\',1)
            targetFileEntry = backupPrefix + splitSD[1]
            logMessage = 'Backing up --> ' + sourceFileEntry + '\n'
            myTuple = (logHandle, logMessage)
            QbLflag = write_to_logfile(myTuple)
            copy2(sourceFileEntry, targetFileEntry)
            totalFilesBackedUp += 1
            totalBytes = totalBytes + sourceSize[sfPointer]
          else :
            if ((sourceMtime[sfPointer] > targetMtime[sfPointer]) or
              (sourceSize[sfPointer] != targetSize[sfPointer])) :
                sourceFileEntry = sourcePath[sfPointer]
                targetFileEntry = targetPath[sfPointer]
                logMessage = 'Backing up ++> ' + sourceFileEntry + '\n'
                myTuple = (logHandle, logMessage)
                QbLflag = write_to_logfile(myTuple)
                copy2(sourceFileEntry, targetFileEntry)            
                totalFilesBackedUp += 1
                totalBytes = totalBytes + sourceSize[sfPointer]
    
    sourceEntries.close()
    targetEntries.close()

logMessage = 'Total number of files backed up = ' + str(totalFilesBackedUp) + '\n'
myTuple = (logHandle, logMessage)
QbLflag = write_to_logfile(myTuple)

if totalBytes != 0 :
    totalBytes = totalBytes / 1024

logMessage = 'Total number of Kbytes backed up = ' + str(totalBytes) + '\n'
myTuple = (logHandle, logMessage)
QbLflag = write_to_logfile(myTuple) 
myTuple = (logHandle, 'Terminating program execution \n')
QbLflag = write_to_logfile(myTuple)
    
exit()