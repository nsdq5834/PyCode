# CopyQB.py
# Version 1.0

# This is a simple utility program to backup specific files, in this case we
# are backing up our Quicken database. The backup copies are going to be 
# encrypted.

# Copy in needed support code

from os import *
from io import open
from filecmp import dircmp
from pyAesCrypt import encryptFile

# Define and initialize some variables we will use.

sourceFile = ''
targetFile = ''
QbSflag = False
QbTflag = False
QbPflag = False
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

  if myLines[0].strip() == "QbPwd" :
    QbPassword = myLines[1].strip()
    QbPflag = True	
  
parmFile.close()

# Trivial test to make sure we have the three parameters we need.

if QbSflag == False or QbTflag == False or QbPflag == False :
  print('Parameter error in a parm file record.')
  exit()

# Check to make sure the directories exist.

if not path.isdir(QbSpath) :
  print(QbSpath, ' is not a directory')
  exit()
  
if not path.isdir(QbTpath) :
  print(QbTpath, ' is not a directory')
  exit()

# We are going to use the dircmp function from filecmp. This will do a
# comparison of the source and target directories. From that we will use
# the left_only property to obtain a list of files that are in the source
# directory, but not in the target directory.

filesNeedingBackup = dircmp(QbSpath,QbTpath,None,None).left_only

# Now that we have the list of files we can iterate over them and back them
# up using the encryptFile method drom pyAesCrypt.

for FNB in filesNeedingBackup :
  sourceFile = QbSpath + FNB
  targetFile = QbTpath + FNB + '.aes'
  encryptFile(sourceFile, targetFile, QbPassword, bufferSize)
  
exit()