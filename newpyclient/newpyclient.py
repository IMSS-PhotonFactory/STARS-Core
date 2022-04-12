
########################################################################
#
# Setup wizard for STARS client in python
# 2018-07-04 (Wed)
#

import sys
import time
import random
import os
import shutil
import re


Template    = "newclient_tmplt.py"
TemplateCfg = "newclient_tmplt.cfg"
KeyMin      = 10
KeyMax      = 18
KeyCount    = 400
DefaultPort = 6057

VAR = {}

# Functions ==========================================================================
def entvar(inval, pval=""):
    """Input parametars from console and set to VAL (parameter variable).

       inval: parametername
       pval:  prompt, inval is used if prpmpt is not set
    """
    if pval == "":
       pval =  "Please enter " + inval.replace("_", " ") + "."
    pval = pval + " (null = cancel) >"
    sys.stdout.write(pval)
    sys.stdout.flush()
    inpval = sys.stdin.readline().rstrip("\n")
    if inpval == "":
        print("Canceled.")
        sys.exit()
    VAR[inval] = inpval
    return(VAR[inval])

def ksg_localtime():
    format = "%Y-%m-%d %H:%M:%S"
    return(time.strftime(format, time.localtime()))

def genfile(source, output):
    f = open(source)
    lines = f.readlines()
    f.close()

    f = open(output, "w")
    for line in lines:
        for ky in VAR.keys():
            line = line.replace("<<" + ky + ">>", VAR[ky])
        f.write(line)
    f.close()

def createkey(filename):
    kcount = KeyCount
    sys.stdout.write("Create key > " + filename + " (" + str(kcount) + " keys).\n")
    if filename == "":
        sys.exit("Error: Bad key file name.")
    f = open(filename, "w")

## Create random keywords
    for kline in range(kcount):
        klen = random.randint(KeyMin, KeyMax)
        for kchar in range(klen):
            rnum = random.randint(0x21, 0x7d)
            if rnum >= 0x60:
                rnum += 1
            f.write(chr(rnum))
        f.write("\n")

    f.close()

#=====================================================================================
def main():
    sys.stdout.write("Make a new STARS client program in Python.\n")

### Input parameters.
    entvar("client_name", "Please enter the client name to make.")
    entvar("stars_server", "Please enter the host name or ip address of the stars server.")
    dir = entvar("install_dir", "Please enter directory for {}.".format(VAR["client_name"]))
#    dir = re.sub(r"~/", os.path.expanduser("~") + "/", dir)


    VAR["DefaultPort"] = str(DefaultPort)
    VAR["Modified"] = ksg_localtime() + " Generated."

### Make directory
    os.mkdir(dir)

### Copy files
    genfile(Template, dir + "/" + VAR["client_name"] + ".py")
    genfile(TemplateCfg, dir + "/" + VAR["client_name"] + ".cfg")
    shutil.copyfile("stars.py", dir + "/stars.py")

### Create keyfile
    createkey(dir + "/" + VAR["client_name"] + ".key")

    sys.stdout.write("Done.\n")
    sys.stdout.write("Plese copy \"" + dir + "/" + VAR["client_name"] + ".key\" to takaserv-lib on "
                 + VAR["stars_server"] + ".\n")
    sys.stdout.write("Hit Enter key.")
    sys.stdout.flush()
    sys.stdin.readline().rstrip("\n")


if __name__ == "__main__":
    main()

