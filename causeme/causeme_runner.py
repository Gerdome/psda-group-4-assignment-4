"""
This script can be used to iterate over the datasets of a particular experiment.
Below you import your function "my_method" stored in the module causeme_my_method.

Importantly, you need to first register your method on CauseMe.
Then CauseMe will return a hash code that you use below to identify which method
you used. Of course, we cannot check how you generated your results, but we can
validate a result if you upload code. Users can filter the Ranking table to only
show validated results.
"""

# Imports
import numpy as np
import json
import zipfile
import bz2
import time
import sys
import os

# Setup a python dictionary to store method hash, parameter values, and results
results = {}

################################################
# Identify method and used parameters
################################################

# Method name just for file saving
method_name = sys.argv[1]

# Insert method hash obtained from CauseMe after method registration
if method_name == 'pcmci':
    from causeme_pcmci import my_method
    callmethod = lambda data: my_method(data, maxlags=5)
    results['method_sha'] = "75af488f97b743b4992ff7a6c7d5956b"
    results['parameter_values'] = "maxlag=5"
elif method_name == 'tcdf':
    from causeme_tcdf import my_method
    callmethod = lambda data: my_method(data, hidden_layers=1)
    results['method_sha'] = "29ca7c9e0d3b444194c2337edafe53fb"
    results['parameter_values'] = "hidden=1"
else:
    sys.exit('Invalid method name!')


#################################################
# Experiment details
#################################################
# Choose model and experiment as downloaded from causeme
results['model'] = sys.argv[2]

# Here we choose the setup with N=3 variables and time series length T=150
experimental_setup = sys.argv[3]
results['experiment'] = results['model'] + '_' + experimental_setup

# Adjust save name if needed
save_name = '{}_{}_{}'.format(method_name,
                            results['parameter_values'],
                            results['experiment'])

# Setup directories (adjust to your needs)
root = '/smartdata/uqeih/causeme/'
if not os.path.isdir(root): # local execution
    root = ''
experiment_zip = root + 'experiments/%s.zip' % results['experiment']
results_file = root + 'results/%s.json.bz2' % (save_name)

#################################################

# Start of script
scores = []
pvalues = []
lags = []
runtimes = []

# (Note that runtimes on causeme are only shown for validated results, this is more for
# your own assessment here)

# Loop over all datasets within an experiment
# Important note: The datasets need to be stored in the order of their filename
# extensions, hence they are sorted here
print("Load data")
with zipfile.ZipFile(experiment_zip, "r") as zip_ref:
    for name in sorted(zip_ref.namelist()):
        print("Run {} on {}".format(method_name, name))
        progress_name = root + 'progress/' + method_name + "_" + name
        f = open(progress_name, 'w')
        f.close()

        data = np.loadtxt(zip_ref.open(name))

        # Runtimes for your own assessment
        start_time = time.time()

        # Run your method (adapt parameters if needed)
        val_matrix, p_matrix, lag_matrix = callmethod(data)
        runtimes.append(time.time() - start_time)

        # Now we convert the matrices to the required format
        # and write the results file
        scores.append(val_matrix.flatten())

        # pvalues and lags are recommended for a more comprehensive method evaluation,
        # but not required. Then you can leave the dictionary field empty          
        if p_matrix is not None: pvalues.append(p_matrix.flatten())
        if lag_matrix is not None: lags.append(lag_matrix.flatten())

        if os.path.exists(progress_name):
            os.remove(progress_name)

# Store arrays as lists for json
results['scores'] = np.array(scores).tolist()
if len(pvalues) > 0: results['pvalues'] = np.array(pvalues).tolist()
if len(lags) > 0: results['lags'] = np.array(lags).tolist()
results['runtimes'] = np.array(runtimes).tolist()

# Save data
print('Writing results ...')
results_json = bytes(json.dumps(results), encoding='latin1')
with bz2.BZ2File(results_file, 'w') as mybz2:
    mybz2.write(results_json)
