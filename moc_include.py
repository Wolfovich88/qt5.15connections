#/usr/bin/python
# -*- coding: UTF-8 -*-
# check_code v1.0
# run from root of repository

import sys
import os

QtMacrosList = [
'Q_OBJECT',
'signals:',
'slots:',
'Q_CLASSINFO',
'Q_PLUGIN_METADATA',
'Q_INTERFACES',
'Q_PROPERTY',
'Q_PRIVATE_PROPERTY',
'Q_REVISION',
'Q_OVERRIDE',
'Q_ENUM',
'Q_FLAGS',
'Q_SCRIPTABLE',
'Q_INVOKABLE',
'Q_SIGNAL',
'Q_SLOT'
]

def _isContainPattern(filename, patternItem):
        inputfile = open(filename,'r')
    	for line in inputfile:
            if type(patternItem) is list:
                for pattern in patternItem:
                    if pattern in line:
                       return True
            else:
                if patternItem in line:
                    return True
        return False

def _appendStringToFile(filename, string):
    if os.path.isfile(filename):
       print "File contains " + str(_isContainPattern(filename, string))
       if not _isContainPattern(filename, string):
           print "Write " + string + " to " + filename
           f = open(filename,'a')
           f.write("\n")
           f.write(string)
           f.write("\n")
           f.close()


def _setFileslist(folder, patternList):
    for root, _dirs, files in os.walk(folder):
        for f in files:
	    ext = f.split(".")[-1]
            name = f.split(".")[0]
	    
            if ext == "h" and _isContainPattern(os.path.join(root, f), patternList):
                namecpp = name + ".cpp"
                fullnamecpp = os.path.join(root, namecpp)
                moc_str = "#include \"moc_" + namecpp + "\""
                _appendStringToFile(fullnamecpp, moc_str)
            
            elif ext == "cpp" and "Engine" in name:
                _appendStringToFile(os.path.join(root, f), "#include \"moc_" + f + "\"")

if __name__ == "__main__":
    if len (sys.argv) != 2:
        print "The script inserts the \"#include moc_filename.cpp\" to all cpp files with any Qt macros."
        print "Run the script with a parameter: <path_to_destination_folder>"
        sys.exit(1)
    
    _setFileslist(sys.argv[1], QtMacrosList)




