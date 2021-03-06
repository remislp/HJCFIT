import time
import math
import sys
import numpy as np
from scipy.optimize import minimize

from dcpyps import dcio
from dcpyps import dataset
from dcpyps import mechanism
from dcprogs.likelihood import Log10Likelihood

# LOAD DATA: Burzomato 2004 example set.
scnfiles = [["../../DCPYPS/dcpyps/samples/glydemo/A-10.scn"], 
            ["../../DCPYPS/dcpyps/samples/glydemo/B-30.scn"],
            ["../../DCPYPS/dcpyps/samples/glydemo/C-100.scn"], 
            ["../../DCPYPS/dcpyps/samples/glydemo/D-1000.scn"]]
tres = [0.000030, 0.000030, 0.000030, 0.000030]
tcrit = [0.004, -1, -0.06, -0.02]
conc = [10e-6, 30e-6, 100e-6, 1000e-6]

recs = []
bursts = []
for i in range(len(scnfiles)):
    rec = dataset.SCRecord(scnfiles[i], conc[i], tres[i], tcrit[i])
    rec.record_type = 'recorded'
    recs.append(rec)
    bursts.append(rec.bursts.intervals())
    rec.printout()

# LOAD FLIP MECHANISM USED Burzomato et al 2004
mecfn = "../../DCPYPS/dcpyps/samples/mec/demomec.mec"
version, meclist, max_mecnum = dcio.mec_get_list(mecfn)
mec = dcio.mec_load(mecfn, meclist[2][0])

# PREPARE RATE CONSTANTS.
#rates = [5000.0, 500.0, 2700.0, 2000.0, 800.0, 15000.0, 300.0, 0.1200E+06, 6000.0, 0.4500E+09, 1500.0, 12000.0, 4000.0, 0.9000E+09, 7500.0, 1200.0, 3000.0, 0.4500E+07, 2000.0, 0.9000E+07, 1000, 0.135000E+08]
rates = [4500.0, 700.0, 2500.0, 1800.0, 900.0, 18000.0, 200.0, 0.1100E+06, 4900.0, 0.4000E+09, 1850.0, 10000.0, 5000.0, 0.7500E+09, 8500.0, 1050.0, 3500.0, 0.5000E+07, 2300.0, 0.9500E+07, 1950, 0.130000E+08]

mec.set_rateconstants(rates)

# Fixed rates.
#fixed = np.array([False, False, False, False, False, False, False, True,
#    False, False, False, False, False, False])
#if fixed.size == len(mec.Rates):
for i in range(len(mec.Rates)):
    mec.Rates[i].fixed = False

# Constrained rates.
mec.Rates[21].is_constrained = True
mec.Rates[21].constrain_func = mechanism.constrain_rate_multiple
mec.Rates[21].constrain_args = [17, 3]
mec.Rates[19].is_constrained = True
mec.Rates[19].constrain_func = mechanism.constrain_rate_multiple
mec.Rates[19].constrain_args = [17, 2]
mec.Rates[16].is_constrained = True
mec.Rates[16].constrain_func = mechanism.constrain_rate_multiple
mec.Rates[16].constrain_args = [20, 3]
mec.Rates[18].is_constrained = True
mec.Rates[18].constrain_func = mechanism.constrain_rate_multiple
mec.Rates[18].constrain_args = [20, 2]
mec.Rates[8].is_constrained = True
mec.Rates[8].constrain_func = mechanism.constrain_rate_multiple
mec.Rates[8].constrain_args = [12, 1.5]
mec.Rates[13].is_constrained = True
mec.Rates[13].constrain_func = mechanism.constrain_rate_multiple
mec.Rates[13].constrain_args = [9, 2]
mec.update_constrains()

mec.set_mr(True, 7, 0)
mec.set_mr(True, 15, 1)

mec.printout(sys.stdout)
theta = np.log(mec.theta())

kwargs = {'nmax': 2, 'xtol': 1e-12, 'rtol': 1e-12, 'itermax': 100,
    'lower_bound': -1e6, 'upper_bound': 0}
likelihood = []

for i in range(len(recs)):
    likelihood.append(Log10Likelihood(bursts[i], mec.kA,
        recs[i].tres, recs[i].tcrit, **kwargs))

def dcprogslik(x, args=None):
    mec.theta_unsqueeze(np.exp(x))
    lik = 0
    for i in range(len(conc)):
        mec.set_eff('c', conc[i])
        lik += -likelihood[i](mec.Q) * math.log(10)
    return lik

iternum = 0
def printiter(theta):
    global iternum
    iternum += 1
    lik = dcprogslik(theta)
    print("iteration # {0:d}; log-lik = {1:.6f}".format(iternum, -lik))
    print(np.exp(theta))

lik = dcprogslik(theta)
print ("\nStarting likelihood (DCprogs)= {0:.6f}".format(-lik))
start = time.clock()
success = False
result = None
while not success:
    #res = minimize(dcprogslik, np.log(theta), method='Powell', callback=printit, options={'maxiter': 5000, 'disp': True})
    result = minimize(dcprogslik, theta, method='Nelder-Mead', callback=printiter,
        options={'xtol':1e-4, 'ftol':1e-4, 'maxiter': 5000, 'maxfev': 10000,
        'disp': True})
    if result.success:
        success = True
    else:
        theta = result.x
        
end = time.clock()
print ("\nDCPROGS Fitting finished: %4d/%02d/%02d %02d:%02d:%02d\n"
        %time.localtime()[0:6])
print ('time in simplex=', end - start)
print ('\n\nresult=')
print (result)

print ('\n Final log-likelihood = {0:.6f}'.format(-result.fun))
print ('\n Number of iterations = {0:d}'.format(result.nit))
print ('\n Number of evaluations = {0:d}'.format(result.nfev))
mec.theta_unsqueeze(np.exp(result.x))
print ("\n Final rate constants:")
mec.printout(sys.stdout)
print ('\n\n')


