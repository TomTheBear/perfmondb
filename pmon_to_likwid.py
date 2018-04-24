#!/usr/bin/env python


import os, json, sys, glob, os.path

folder = "BDX"

def get_files(folder):
    out = []
    p = os.path.join(os.getcwd(), folder)
    cp = os.path.join(p, "*_core*.json")
    flist = sorted(glob.glob(cp))
    out.append(flist[-1])
    cp = os.path.join(p, "*_uncore*.json")
    flist = sorted(glob.glob(cp))
    out.append(flist[-1])
    return out

def analyse_file(f):
    o = []
    fp = open(f, "r")
    j = json.load(fp)
    for e in j:
        c = "NONE"
        if e["Counter"].startswith("Fixed"):
            c = "FIXC" + e["Counter"][-1]
        elif e["Counter"] == "0,1,2,3":
            c = "PMC"
        elif e["Counter"] and not "UNC_" in e["EventName"]:
            c = "PMC" + e["Counter"]
        else:
            print(e)
        x = {"Name" : e["EventName"], "Event" : e["EventCode"], "Umask" :
                e["UMask"], "Limit" : c}
        o.append(x)
    return o

flist = get_files(folder)
out = []
for f in flist:
    out += analyse_file(f)
    break
print(out)
