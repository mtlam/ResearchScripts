import psrcat
import os
import sys
import subprocess


psr = str(sys.argv[1])

d = psrcat.psrcat(psr,["Gl","Gb","DM"])


DIR='/home/michael/Research/Programs/NE2001/bin.NE2001/'
cwd = os.getcwd()
os.chdir(DIR)
cmd = './NE2001 %s %s %s %i' % (d['Gl'],d['Gb'],d['DM'],1)
proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,encoding="ascii")
for line in proc.stdout:
    print line[:-1]
os.chdir(cwd) #not necessary
