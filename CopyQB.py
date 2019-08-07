# CopyQB.py

"""
This is a simple utility program to backup specific files, in this case we
are backing up our Quicken database.
"""

from os import *
from io import *
from shutil import *
from stat import *

QbSflag = False
QbTflag = False

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

# Now we test to see if we can obtain the contents of the directories.			
try:
  SD = scandir(QbSpath)
except OSError:
  print('Unable to scan the directory', QbSpath)
  exit()

try:
  TD = scandir(QbTpath)
except OSError:
  print('Unable to scan the directory', QbTpath)



#Need to get pyAesCrypt so we can encrypt files prior to placing on cloud
#Grab it from pypi.org

