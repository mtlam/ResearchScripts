'''
Example:
psrstat -c nchan,nsubint filename
-> psrstat(filename,"nchan,nsubint")
-> psrstat(filename,["nchan","nsubint"])
-> psrstat(filename,np.ndarray(["nchan","nsubint"]))
Returns a list
'''


import subprocess
import numpy as np
import re


def psrstat(filename,parameters):
    if not isinstance(parameters,(str,list,np.ndarray)):
        raise ValueError("Bad parameter type")
    if type(parameters) != type(""):
        parameters = ",".join(parameters)

    cmd = 'psrstat -Q -c %s %s' % (parameters,filename)
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    out, err = proc.communicate()

    retval = out.split()[1:]
    for i,item in enumerate(retval):
        if item.isdigit():
            retval[i] = int(item)
        else:
            try:
                retval[i] = float(item)
            except ValueError:
                continue
    return retval
  
