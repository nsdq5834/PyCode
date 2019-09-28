# sfbkup.py
# Version 1.00


# Look here for logging examples. 
# https://docs.python.org/3/howto/logging-cookbook.html

# Python program to create backups of files. The list of files to be backed
# is specified in the sfbkup.parms file. This file contains a list of direc-
# tories that will be scanned to build a list of the files that need to be
# backed up.

# The program is invoked with a single parameter which provides the base
# location for the logging file.
#
# Example  C:\sfbkup D:\Logs\

# Copy in needed support code

from os import *
from sys import setrecursionlimit, argv
from io import open
from shutil import copy2
from filecmp import dircmp
from datetime import datetime
from math import ceil
import logging

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

# Define and initialize some constants and variables we will use.

kiloBytes = 1024
megaBytes = kiloBytes * 1024
gigaBytes = megaBytes * 1024

QbEflag = False
QbSflag = False
QbBflag = False
EnumFlag = False

baseDirect = []
baseExcept = []
sourceDirect = []
targetDirect = []

sourceFile = []
sourcePath = []
sourceMtime = []
sourceSize = []

targetFile = []
targetPath = []
targetMtime = []
targetSize = []

# We will use the built-in Python logging facility.
# Construct the log file name

logFileBase = argv[1]
logNameBase = path.splitext(path.basename(argv[0]))[0]
logPathBase = logFileBase + logNameBase + '\\' +logNameBase + '_'
rightNow = datetime.now()
logFile = logPathBase + rightNow.strftime("%Y%m%d_%H%M%S") + ".log"

# Create logging file with specific parameters.

logging.basicConfig(filename=logFile,
                   filemode='w',
                   format='%(asctime)s %(module)s %(levelname)s %(message)s',
                   datefmt='%m/%d/%Y %H:%M:%S',
                   level=logging.DEBUG)
                   
# Write opening line to our logger file.
                   
logging.info('Begin program execution')

# See if we can open the parameter file.

try:
    parmFile = open("sfbkup.parms","r",1)
except PermissionError:
    logging.error('Access permission error reading parameter file.')
    exit()
except FileNotFoundError:
    logging.error('Parameter file does not exist or not found.')
    exit()
else:
    logging.info('Parameter file opened for procession.')

# Read and process the parameter file. Very simple logic to isolate the
# parameters we need. We set the recursion limit before we read the parm
# file. Use a simple if ladder to isolate our parameters.

recursionLimit = 5000

for lines in parmFile:

    if lines[:1] != '#' :

      myLines = lines.split("=",2)
  
      if myLines[0].strip() == "BackupSource" :
        QbSpath = myLines[1].strip()
        QbSflag = True

      if myLines[0].strip() == "ExcludeSource" :
        QbEpath = myLines[1].strip()
        QbEflag = True

      if myLines[0].strip() == "BackupBaseLocation" :
        QbBackupLoc = myLines[1].strip()
        QbBflag = True
        
      if myLines[0].strip() == "RecursionLimit" :
        recursionLimit = int(myLines[1].strip())
  
parmFile.close()

# Trivial test to make sure we have the four parameters we need.

if (QbEflag == False or QbSflag == False or
    QbBflag == False) :
      logging.error('Parameter error in a parm file record.')
      exit()

logging.info('Parameter file has been read and processed')

# Now set the recursion limit.

setrecursionlimit(recursionLimit)

logMessage = 'Recursion limit has been set to ' + str(recursionLimit)
logging.info(logMessage)
  
logging.info('Processing records from source directory file.')

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
    pass
    
for lines in BkSrc :
  baseDirect.append(lines.strip())
  linesRead += 1
  
BkSrc.close()

logMessage = 'Number of base directories = ' + str(linesRead)
logging.info(logMessage)

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
    pass
    
for lines in BkExc :
  baseExcept.append(lines.strip())
  linesRead += 1
  
BkExc.close()

logMessage = 'Number of directories to exclude = ' + str(linesRead)
logging.info(logMessage)

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

logMessage = 'Total number of directories to process = ' + str(len(sourceDirect))
logging.info(logMessage)

sourceDirect.sort()

logging.info('Source directory list has been sorted.')

# Now create the list of target directories.

sourceTotal = 0

for SD in sourceDirect :
    splitSD = SD.split('\\', 1)
    BD = QbBackupLoc + splitSD[1]
    targetDirect.append(BD)
    sourceTotal += 1  

#targetTotal = sourceTotal

logging.info('Target directory list has been built.')
logging.info('Checking for the existence of target directories.')

#
# Next we will iterate through the list of target directories directories to
# make sure they all exist. If we get a FileNotFoundError we will go ahead and
# create the target directory.
#

for TD in targetDirect :
    try :
      scandir(TD)
    except FileNotFoundError :
      mkdir(TD)
      logMessage = 'Directory created = ' + TD
      logging.info(logMessage)

logging.info('Completed checking/creating target directories.')

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
    tdFlag = False

    try:
      sourceEntries = scandir(sourceDirect[sourcePointer])
    except NotADirectoryError :
      pass
    except PermissionError :
      pass
    else :
      seCounter = 0
      sourceFile.clear()
      sourcePath.clear()
      sourceMtime.clear()
      sourceSize.clear()
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
      try:
        targetEntries = scandir(targetDirect[sourcePointer])
      except NotADirectoryError :
        pass
      except PermissionError :
        pass
      else :
        targetFile.clear()
        targetPath.clear()
        targetMtime.clear()
        targetSize.clear()
        for TE in targetEntries :
          if TE.is_file() :
            targetFile.append(TE.name)
            targetPath.append(TE.path)
            statVals = TE.stat()
            targetMtime.append(statVals.st_mtime)
            targetSize.append(statVals.st_size)
            tdFlag = True
      
      if sdFlag and not tdFlag :
        for sfPointer in range(seCounter) :
          sourceFileEntry = sourcePath[sfPointer]
          splitSD = sourceFileEntry.split('\\',1)
          targetFileEntry = QbBackupLoc + splitSD[1]
          try :
            copy2(sourceFileEntry, targetFileEntry)
          except PermissionError :
            logMessage = 'PermissionError --> ' + sourceFileEntry
            logging.error(logMessage)
          else :
            logMessage = 'Backing up --> ' + sourceFileEntry
            logging.info(logMessage)
            totalFilesBackedUp += 1
            totalBytes += sourceSize[sfPointer]
            
      if sdFlag and tdFlag :
        for sfPointer in range(seCounter) :
          try :
            tfPointer = targetFile.index(sourceFile[sfPointer])
          except ValueError :
            sourceFileEntry = sourcePath[sfPointer]
            splitSD = sourceFileEntry.split('\\',1)
            targetFileEntry = QbBackupLoc + splitSD[1]
            try :
              copy2(sourceFileEntry, targetFileEntry)
            except PermissionError :
              logMessage = 'PermissionError --> ' + sourceFileEntry
              logging.error(logMessage)
            else :
              logMessage = 'Backing up --> ' + sourceFileEntry
              logging.info(logMessage)               
              totalFilesBackedUp += 1
              totalBytes += sourceSize[sfPointer]
          else :
            if ((sourceMtime[sfPointer] != targetMtime[tfPointer]) or
              (sourceSize[sfPointer] != targetSize[tfPointer])) :
                sourceFileEntry = sourcePath[sfPointer]
                targetFileEntry = targetPath[sfPointer]
                try :
                  copy2(sourceFileEntry, targetFileEntry)
                except PermissionError :
                  logMessage = 'PermissionError --> ' + sourceFileEntry
                  logging.error(logMessage)
                else :
                  logMessage = 'Backing up --> ' + sourceFileEntry
                  logging.info(logMessage)               
                  totalFilesBackedUp += 1
                  totalBytes += sourceSize[sfPointer]
    
    sourceEntries.close()
    targetEntries.close()

logMessage = 'Total number of files backed up = ' + str(totalFilesBackedUp)
logging.info(logMessage)

# Some simple logic to output a message about to size of the backups.

unitStorage = 'Bytes'
unitDivisor = 1

if totalBytes != 0 :
    if totalBytes > kiloBytes :
      unitStorage = 'KiloBytes'
      unitDivisor = kiloBytes
    if totalBytes > megaBytes :
      unitStorage = 'MegaBytes'
      unitDivisor = megaBytes
    if totalBytes > gigaBytes :
      unitStorage = 'GigaBytes'
      unitDivisor = gigaBytes
    totalBytes = ceil(totalBytes / unitDivisor)

logMessage = 'Total number of ' + unitStorage + ' backed up = ' + str(totalBytes)
logging.info(logMessage)

logging.info('Terminating program execution')
    
exit()