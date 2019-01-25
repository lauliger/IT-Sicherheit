import os
import logging
import sys
import json

logging.basicConfig(level=logging.DEBUG)

from rekall import session
from rekall import plugins

class cl:
    PINK = '\033[95m'
    LBLUE = '\033[94m'
    BLUE = '\033[92m'
    YELLOW = '\033[93m'
    ORANGE = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

s = session.Session(
    filename=str(sys.argv[1]),
    autodetect=["rsds"],
    logger=logging.getLogger(),
    autodetect_scan_length=18446744073709551616,
    profile_path=[
    "http://profiles.rekall-forensic.com"
    ])

def getPsList():
    getResp = s.plugins.pslist()
    return getResp

def fileCheck():
    getResp = s.plugins.imageinfo()
    if("RuntimeError: Unable to find" in getResp):
        return False
    else:
        print("+++++++++++++++++++")
        return True

class process(object):
    def __init__(self, offset, name, ppid, create_time):
        self.offset = offset
        self.name = name
        self.ppid = ppid
        self.create_time = create_time

def genList(src):
    out = []
    buff = []
    processlist = []
    for c in src:
        if c == '\n':
            out.append(''.join(buff))
            buff = []
        else:
            buff.append(c)
    for i in range(2,len(out)-1):
        tmpStr = out[i].split()
        print(tmpStr)
        tmpObj = process(tmpStr[0], tmpStr[1], tmpStr[2].replace("(","").replace(")",""), tmpStr[8])
        processlist.append(tmpObj)
    return processlist

def getPriority(src):
    getPrio = s.plugins.SELECT(_EPROCESS.name, _EPROCESS.pid, _EPROCESS.Pcb.BasePriority FROM pslist() WHERE regex_proc("lsass.exe", _EPROCESS.name))
    
def exportToJson(listOfObjects, pathToJson):
    outFile = open(pathToJson, "w")
    jsonList = json.dumps(listOfObjects, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    outFile.write(jsonList)
    outFile.close()

def exportToJsonWithExceptionIDs(listOfObjects, exception, pathToJson):
    generatedList = []
    for p in range(0, len(listOfObjects)-1):
        if(str(listOfObjects[p].ppid) not in exception):
            generatedList.append(listOfObjects[p])
    print("[+] Excludet: " + str(int(len(listOfObjects)-len(generatedList))) + " Objects!")
    exportToJson(generatedList, pathToJson)

def importFromJson(pathToJson):
    print()

if __name__ == '__main__':
    print(fileCheck())
    print(getPsList())
    print("\n\n\n")
    exportToJsonWithExceptionIDs(genList(str(s.plugins.pslist())),["868","1928"], "./ausgabe.json")
    #exportToJson(genList(str(s.plugins.pslist())), "./ausgabe.json")
