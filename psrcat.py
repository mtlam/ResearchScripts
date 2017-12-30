'''
Script to run and parse psrcat command line output
'''

import subprocess
import numpy as np


ALL = "J*"


def psrcat(psrname,parameters,error=False):#,rettype="dict"):
    if type(psrname)==type([]) or type(psrname)==np.ndarray:
        return psrcatlist(psrname,parameters)

    if type(parameters)==type([]) or type(parameters)==np.ndarray:
        parameterslist = parameters
        parameters = " ".join(parameters)
    else:
        parameterslist = parameters.split()
        
    if error:
        cmd = 'psrcat -o long_error -c "%s" %s' % (parameters,psrname)
    else:
        cmd = 'psrcat -c "%s" %s' % (parameters,psrname)
    #print cmd
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    out, err = p.communicate()
    lines = out.split('\n')
    if lines[0][:7]=="WARNING":
        raise ValueError(lines[0])

    header = lines[1]
    units = lines[2]
    entries = np.array(lines[4:-2])

    
    inds = np.where(entries!="")[0]
    entries = entries[inds]
  

    if len(entries) > 1:
        retval = dict()
        for i,entry in enumerate(entries):
            retval[i] = dict()
            for param in parameterslist:
                try: 
                    index = header.index(param)
                except ValueError:
                    index = units.index(param) #attempt to see if it's in the second line

                if error:
                    val = entry[index:].split()[1]
                else:
                    val = entry[index:].split()[0]
                retval[i][param] = val

    else:
        retval = dict()
        entry = entries[0]
        for param in parameterslist:
            try:
                index = header.index(param)
            except ValueError:
                index = units.index(param) #attempt to see if it's in the second line
            if error:
                val = entry[index:].split()[1]
            else:
                val = entry[index:].split()[0]
            retval[param] = val
            
    for key in retval.keys():
        if retval[key] == '*':
            retval[key] = None

    return retval



def psrcatlist(psrnames,parameters):
    if type(psrnames)==type([]) or type(psrnames)==np.ndarray:
        psrnameslist = psrnames
    else:
        psrnameslist = psrnames.split()
    if type(parameters)==type([]) or type(parameters)==np.ndarray:
        parameterslist = parameters
        parameters = " ".join(parameters)
    else:
        parameterslist = parameters.split()

    retval = dict()

    for name in psrnameslist:
        try:
            val = psrcat(name,parameters)
            retval[name] = val
        except ValueError:
            continue
    return retval



def psrcatlistold(psrnames,parameters,rettype="dict"):
    if type(psrnames)==type([]) or type(psrnames)==np.ndarray:
        psrnameslist = psrnames
        psrnames = " ".join(psrnames)
    else:
        psrnameslist = psrnames.split()
    if type(parameters)==type([]) or type(parameters)==np.ndarray:
        parameterslist = parameters
        parameters = " ".join(parameters)
    else:
        parameterslist = parameters.split()
        
    cmd = 'psrcat -c "%s" %s' % (parameters,psrnames)
    print cmd
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
    out, err = p.communicate()
    lines = out.split('\n')
    if lines[0][:7]=="WARNING": #must run them separately
        return psrcatlist(psrnames,parameters)
    header = lines[1]
    units = lines[2]
    entries = np.array(lines[4:-2])

    
    
    #for entry in allentr
    inds = np.where(entries!="")[0]
    entries = entries[inds]
    
    if rettype == 'dict':
        retval = dict()
        for name in psrnameslist:
            retval[name] = dict()


    for param in parameterslist:
        index = header.index(param)

        for i,entry in enumerate(entries): 
            #print i,entry
            retval[psrnameslist[i]][param] = entry[index:].split()[0]

    return retval


#example: psrcat.psrcat(psr,"P0")["P0"]
def getValue(psr,parameter):
    return psrcat(psr,parameter)[parameter]
def getValueList(psrs,parameter):
    return map(lambda psr: getValue(psr,parameter),psrs)


# Helper to grab single parameter out of lists
def paramToList(dictionary,parameter,sort=True):
    keys = np.array(dictionary.keys())
    values = np.array(map(lambda x: dictionary[x][parameter],dictionary))
    if sort:
        inds = np.argsort(keys)
        return keys[inds],values[inds]
    return keys,values




#test:
if __name__=="__main__":
    #print psrcat(["J1713+0747","J2317+1439"],["P0","F0","BSURF_I"])
    print psrcat("J1713+0747",["P0","BSURF_I"])
    #print psrcat("J1824-2452",["P0","BSURF_I"])

    x=psrcat(np.array(['J0358+5413', 'J0502+4654', 'J0525+1115', 'J0543+2329',
       'J1543+0929', 'J1705-1906', 'J1735-0724', 'J1745-3040',
       'J1759-2205', 'J1824-2452', 'J1847-0402', 'J1851+1259',
       'J1909+1102', 'J1935+1616', 'J2013+3845', 'J2023+5037',
       'J2037+3621', 'J2048-1616', 'J2326+6113', 'J0437-4715',
       'J0613-0200', 'J1024-0719', 'J1045-4509', 'J1600-3053',
       'J1603-7202', 'J1643-1224', 'J1730-2304', 'J1732-5049',
       'J1824-2452', 'J1857+0943', 'J1909-3744', 'J1939+2134',
       'J2124-3358', 'J2145-0750', 'J0835-4510', 'J0908-4913',
       'J1824-1945', 'J1833-0827', 'J0834-4159', 'J1702-4128',
       'J1721-3532', 'J1745-3040', 'J1809-1917', 'J1826-1334']),"BSURF_I")
    print x
