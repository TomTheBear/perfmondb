#!/usr/bin/env python3

import os, glob, os.path, re

files = {"IVB" : "index/ivybridge.html",
         "CLX" : "index/cascadelake_server.html",
         "IVT" : "index/ivytown.html",
         "ICL" : "index/icelake.html",
         "GLM" : "index/goldmont.html",
         "SLM" : "index/silvermont.html",
         "GLP" : "index/goldmontplus.html",
         "BDW" : "index/broadwell.html",
         "HSW" : "index/haswell.html",
         "BDW-DE" : "index/broadwell_server.html",
         "BDX" : "index/broadwell_server.html",
         "BNL" : "index/atom.html",
         "HSX" : "index/haswell_server.html",
         "JKT" : "index/snbep.html",
         "KNL" : "index/knl.html",
         "KNM" : "index/knl.html",
         "NHM-EP" : "index/corei7.html",
         "NHM-EX" : "index/corei7b.html",
         "WSM-EP-DP" : "index/corei7wdp.html",
         "WSM-EP-SP" : "index/corei7wsp.html",
         "WSM-EX" : "index/wsmex.html",
         "SKL" : "index/skylake.html",
         "SKX" : "index/skylake_server.html",
         "SNB" : "index/snb.html", 
         "SNR" : None}


outfile = "index.html"

out = open(outfile, "w")


out.write(""" <!DOCTYPE html>
<html>
<head>
<title>Performance Monitoring event lists for Intel processors</title>
</head>
<body>\n""")

for s in files:
    p = files[s]
    head = None
    if p:
        with open(p, "r") as fp:
            data = fp.read()
            m = re.search("<h3>(.*)</h3>", data)
            if m:
                head = m.group(1)
    if p and head and s:
        out.write("<h1><a href={}>{}</a></h1>\n".format(p, head))
        folderfiles = sorted(glob.glob(os.path.join(s, "*.json")))
        m = re.search(".*_([vV][\d\.]+).*\.json", folderfiles[-1])
        if m:
            folderfiles = sorted(glob.glob(os.path.join(s, "*{}*.json".format(m.group(1)))))
            for f in folderfiles:
                out.write("<p><a href={}>{}</a></p>\n\n".format(f, os.path.basename(f)))

out.write("""</body>\n</html>\n""")
