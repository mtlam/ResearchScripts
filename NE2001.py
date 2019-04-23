'''
Commands to run NE2001 and grab results
'''
import subprocess
import os
import sys
import warnings

if sys.version_info.major == 2:
    fmap = map    
elif sys.version_info.major == 3:
    fmap = lambda x,*args: list(map(x,*args))
    xrange = range


def NE2001(l,b,DM_D,ndir=1,DIR='/home/michael/Research/Programs/NE2001/bin.NE2001/'):
    cwd = os.getcwd()
    os.chdir(DIR)
    cmd = './NE2001 %f %f %f %i' % (l,b,DM_D,ndir)
    proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    output = [line.strip() for line in proc.stdout]
    output = output[6:]
    try:
        values = fmap(lambda x: float(x.split()[0]),output)
    except ValueError: #distance has ">" symbol
        values = list()
        values.append(float(output[0].split()[1]))
        values.extend(fmap(lambda x: float(x.split()[0]),output[1:]))
        warnings.warn("Warning: Distance is a lower limit")
    retval = dict()
    retval['input'] = dict()
    retval['input']['l'] = l
    retval['input']['b'] = b
    retval['input']['DM/D'] = DM_D
    retval['input']['ndir'] = ndir
    retval['output'] = dict()
    varlist = ['DIST','DM','DMz','SM','SMtau','SMtheta','SMiso','EM','TAU','SBW','SCINTIME','THETA_G','THETA_X','NU_T']
    for i,var in enumerate(varlist):
        retval['output'][var] = values[i]
    os.chdir(cwd)
    return retval


if __name__=='__main__':
    if len(sys.argv) == 1:
        print(NE2001(45,5,50,1))#Just test it out
    elif len(sys.argv) == 5:
        args = fmap(lambda x: float(x),sys.argv[1:])
        print(NE2001(*args))

