#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os

def _getLeadingSpaces(line):
    spaces = ""
    for i in line:
        if i == ' ':
            spaces+=i
        else:
            break
    return spaces
    
def _addCppOwnership(filename):
    f = open(filename, 'r+')
    content = f.readlines()
    f.seek(0)
    headerSectionDone = False
    insideConnectionHandler = False
    changesCount = 0
    
    for line in content:
              
        if "#ifndef HCAT_DESIGNER" in line and headerSectionDone == False:
            newLine = "#include <QQmlEngine>\n"
            f.write(line)
            f.write(newLine)
            headerSectionDone = True;
            changesCount+=1
            continue
            
        if "Q_UNUSED(qmlEngine)" in line:
            changesCount+=1
            continue

        if "source = Frm::Bridge::instance()->getFeatureSource<" in line:
            newLine = _getLeadingSpaces(line) + "qmlEngine->setObjectOwnership(source, QQmlEngine::CppOwnership);\n"
            f.write(line)
            f.write(newLine)
            changesCount+=1
            continue
        
        f.write(line)
            
    f.truncate()
    f.close()
    return changesCount

if __name__ == "__main__":
    if len (sys.argv) != 2:
        print ("The script changes ownership to C++ in all source signletones provider classes")
        print ("Run the script with a parameter: <path_to_destination_folder>")
        sys.exit(1)

    for root, _dirs, files in os.walk(sys.argv[1]):
        for f in files:
            ext = f.split(".")[-1]
            if ext == "cpp" and "Provider" in f:
                count = _addCppOwnership(os.path.join(root, f))
                if count > 0:
                    print ("Made %s changes in file %s" % (count, f)) 
