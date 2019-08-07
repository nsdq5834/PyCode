# CopyQB.py

"""
This is a simple utility program to backup specific files, in this case we
are backing up our Quicken database.
"""

from os import *
from io import *
from shutil import *
from stat import *
from filecmp import dircmp

sourceFile = ''
targetFile = ''
QbSflag = False
QbTflag = False
SDfiles = []
TDfiles = []

try:
    parmFile = open("CopyQB.parms","r",1)
except PermissionError:
    print('Access permission error')
except FileNotFoundError:
    print('File does not exist or not found')
else:
    isReadable = parmFile.readable()


for lines in parmFile:

  myLines = lines.split("=",2)
  
  if myLines[0].strip() == "QbSrc" :
    QbSpath = myLines[1].strip()
    QbSflag = True
	
  if myLines[0].strip() == "QbTgt" :
    QbTpath = myLines[1].strip()
    QbTflag = True	
  
parmFile.close()

# Trivial test to make sure we have the two parameters we need.

if QbSflag == False or QbTflag == False :
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
# up using the copy2 method from shutil.

for FNB in filesNeedingBackup :
  sourceFile = QbSpath + FNB
  targetFile = QbTpath + FNB
  copy2(sourceFile, targetFile)




#Need to get pyAesCrypt so we can encrypt files prior to placing on cloud
#Grab it from pypi.org

