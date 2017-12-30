'''
Code for computing a simple CCF. No error propagation is taken into account.
'''

import numpy as np

#Built like acf_unequal
def ccf_unequal(tx,x,ty,y,dtau=1):
    MAX = max(np.max(tx),np.max(ty))
    MIN = min(np.min(tx),np.min(ty))
    num_lags = np.ceil((MAX - MIN)/dtau) + 1 #+1?
    taus = np.arange(num_lags) * dtau

    taus = np.concatenate((-1*taus[::-1][:-1],taus)) #positive and negative lags
    num_lags = len(taus)
    tau_edges = (taus[:-1] + taus[1:])/2.0
    tau_edges = np.hstack((tau_edges,[tau_edges[-1]+dtau]))
    N_taus = np.zeros(num_lags)
    retval = np.zeros(num_lags)

    # this could be sped up several ways
    for i in xrange(len(x)):
        for j in xrange(len(y)):
            #dt = np.abs(tx[i]-ty[j])
            dt = tx[i]-ty[j]
            index = np.where(dt < tau_edges)[0][0]

            N_taus[index] += 1
            retval[index] += x[i]*y[j]
    

    #divide by zero problem!
    retval = retval / N_taus

    return taus,retval
