from sys import argv
import os

class cl:
 HEADER = '\033[95m'
 OKBLUE = '\033[94m'
 OKGREEN = '\033[92m'
 WARNING = '\033[93m'
 FAIL = '\033[91m'
 ENDC = '\033[0m'
 BOLD = '\033[1m'
 UNDERLINE = '\033[4m'


def cmpStrings():
 #Get List1
 print("[ ] get strings of "+argv[1])
 cmdReturn = os.popen("strings "+argv[1]).read()
 firstList = buildList(cmdReturn)
 print(cl.OKGREEN+"[+] "+str(argv[1])+" converted to a list..."+cl.ENDC)
 print("[ ] get strings of "+argv[2])
 cmdReturn = os.popen("strings "+argv[2]).read()
 secondList = buildList(cmdReturn)
 print(cl.OKGREEN+cl.BOLD+"[+] "+argv[2]+" converted to a list..."+cl.ENDC)
 for c in secondList:
     if(c in firstList):
         print("[+] "+c)
     else:
         print(cl.FAIL+"[!] "+c+cl.ENDC)

def buildList(myString):
 out=[]
 actualStr=''
 for c in str(myString):
     if c != '\n':
         actualStr += c
     else:
         out.append(actualStr)
         actualStr = ''
 return out

if __name__=="__main__":
 print("Start")
 cmpStrings()
