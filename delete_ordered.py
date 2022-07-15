#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os

def _searchAndDeleteString(filename):
    f = open(filename, 'r+')
    content = f.readlines()
    f.seek(0)
    for line in content:
        if "CONFIG" in line and "ordered" in line:
            print "Delete: " + line + " from file " + filename
            continue
        else:
            f.write(line)
    f.truncate()
    f.close()

if __name__ == "__main__":
    if len (sys.argv) != 2:
        print "The script deletes given string"
        print "Run the script with a parameter: <path_to_destination_folder>"
        sys.exit(1)

    for root, _dirs, files in os.walk(sys.argv[1]):
        for f in files:
            ext = f.split(".")[-1]
            if ext == "pro" or ext == "pri":
                _searchAndDeleteString(os.path.join(root, f))
