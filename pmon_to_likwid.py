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

opt_dict = { "Invert"       : "EVENT_OPTION_INVERT",
             "EdgeDetect"   : "EVENT_OPTION_EDGE",
             "CounterMask"  : "EVENT_OPTION_THRESHOLD",
             "AnyThread"    : "EVENT_OPTION_ANYTHREAD"}

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
        opts = []
        for opt in opt_dict:
            if e[opt] != "0":
                opts.append("%s=0x%X" % (opt_dict[opt], int(e[opt])))
        if len(opts) > 0:
            x.update({"DefaultOpts" : ",".join(opts)})
        o.append(x)
    return o

def printout(l):
    for e in l:
        elist = e["Event"].split(",")
        
        for i, c in enumerate(elist):
            ename = e["Name"].split(".")[0]
            tname = e["Name"].replace(".", "_")
            if len(elist) > 1:
                tname = tname.replace(ename, ename + "_" + str(i))
                ename = ename + "_" + str(i)

            print "EVENT_%s\t\t%s\t%s" % (ename, c.strip(), e["Limit"])
            if "DefaultOpts" in e:
                print "DEFAULT_OPTIONS_%s\t%s" % (tname, e["DefaultOpts"],)
            print "UMASK_%s\t%s" % (tname, e["Umask"],)
            print

flist = get_files(folder)
out = []
for f in flist:
    out += analyse_file(f)
    break
#print(out)
printout(out)
