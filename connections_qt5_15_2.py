#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os

def commonCondition(line):
    return " on" in line and "target:" not in line and "console." not in line and "function " not in line and "//" not in line and "showToast" not in line and "qsTr" not in line

def condition(line):
    return ": {" in line and commonCondition(line)

def condition2(line):
    return "{" not in line and commonCondition(line)

def _changeConnectionsSyntax(filename):
    f = open(filename, 'r+')
    content = f.readlines()
    f.seek(0)
    insideConnection = False
    insideHandlerLevel = 0
    changesCount = 0
    
    for line in content:
              
        if "Connections" in line and "{" in line:
            insideConnection = True;
        
        if insideConnection == True and condition(line):
            insideHandlerLevel += 1
            newLine = line.replace(" on", " function on", 1)
            newLine = newLine.replace(":", "()", 1)
            f.write(newLine)
            changesCount += 1
            continue
        
        elif insideConnection == True and condition2(line):
            newLine = line.replace(" on", " function on")
            newLine = newLine.replace(":", "() {", 1)
            newLine = newLine.replace("\n", " }\n", 1)
            f.write(newLine)
            changesCount += 1
            continue
        
        f.write(line)
            
        if insideConnection == True and insideHandlerLevel >= 0 and "{" in line:
            insideHandlerLevel += 1
        if insideConnection == True and insideHandlerLevel > 0 and "}" in line:
            insideHandlerLevel -= 1
        
        if insideConnection == True and insideHandlerLevel <= 0 and "}" in line:
            insideConnection = False
            
    f.truncate()
    f.close()
    return changesCount

if __name__ == "__main__":
    if len (sys.argv) != 2:
        print ("The script changes old Connections systax to new (for Qt5.15 and later) in all qml files in a given directory")
        print ("Also it change import QtQuick 2.* version to QtQuick 2.15 (actually not)")
        print ("Run the script with a parameter: <path_to_destination_folder>")
        sys.exit(1)

    for root, _dirs, files in os.walk(sys.argv[1]):
        for f in files:
            ext = f.split(".")[-1]
            if ext == "qml":
                count = _changeConnectionsSyntax(os.path.join(root, f))
                if count > 0:
                    print ("Made %s changes in file %s" % (count, f)) 
