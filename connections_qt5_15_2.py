#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os

def spaceTabCondition(line):
    print(line)
    tmp = line.split("on", 1)[0]
    tmp.replace("\t", " ")
    return tmp.isspace()

def commonCondition(line):
    return (" on" in line or "\ton" in line) and "target:" not in line and "function " not in line and spaceTabCondition(line)

def condition(line):
    return (": {" in line or ":{" in line) and commonCondition(line)

def condition2(line):
    return "{" not in line and commonCondition(line)


def _changeConnectionsSyntax(filename):
    f = open(filename, 'r+', encoding="utf8")
    #print("Opening file: " + filename)
    content = f.readlines()
    f.seek(0)
    insideConnection = False
    insideHandlerLevel = 0
    changesCount = 0
    
    for line in content:
              
        if "Connections" in line and "{" in line: #TODO: comment the "and "{" in line" to change syntax in wrog written Connections with "{" symbol on the next string, then fix it to Connections {
            insideConnection = True
        
        if insideConnection == True and condition(line):
            insideHandlerLevel += 1
            newLine = line.replace(" on", " function on", 1)
            newLine = line.replace("\ton", "\tfunction on", 1)
            newLine = newLine.replace(":{", ": {", 1)
            newLine = newLine.replace(":", "()", 1)
            f.write(newLine)
            changesCount += 1
            continue
        
        elif insideConnection == True and condition2(line):
            newLine = line.replace(" on", " function on", 1)
            newLine = line.replace("\ton", "\tfunction on", 1)
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
        print ("Also it changes import QtQuick 2.* version to QtQuick 2.15 (actually not)")
        print ("Run the script with a parameter: <path_to_destination_folder>")
        sys.exit(1)

    for root, _dirs, files in os.walk(sys.argv[1]):
        for f in files:
            ext = f.split(".")[-1]
            if ext == "qml":
                count = _changeConnectionsSyntax(os.path.join(root, f))
                if count > 0:
                    print ("Made %s changes in the file %s" % (count, f))
