"""
This file must contain a function called my_method that triggers all the steps 
required in order to obtain

 *val_matrix: mandatory, (N, N) matrix of scores for links
 *p_matrix: optional, (N, N) matrix of p-values for links; if not available, 
            None must be returned
 *lag_matrix: optional, (N, N) matrix of time lags for links; if not available, 
              None must be returned

Zip this file (together with other necessary files if you have further handmade 
packages) to upload as a code.zip. You do NOT need to upload files for packages 
that can be imported via pip or conda repositories. Once you upload your code, 
we are able to validate results including runtime estimates on the same machine.
These results are then marked as "Validated" and users can use filters to only 
show validated results.

Shown here is a vector-autoregressive model estimator as a simple method.
"""

import numpy as np
import pandas as pd
import TCDF

cuda = False # 'Use CUDA (GPU) (default: False)')
 #, help='Number of epochs (default: 1000)')
kernel_size = 6 #, help='Size of kernel, i.e. window size. Maximum delay to be found is kernel size - 1. Recommended to be equal to dilation coeffient (default: 4)')
 #, help='Number of hidden layers in the depthwise convolution (default: 0)') 
 #, help='Learning rate (default: 0.01)')
optimizer = 'Adam' #, choices=['Adam', 'RMSprop'], help='Optimizer to use (default: Adam)')
log_interval = 500 #, help='Epoch interval to report loss (default: 500)')
seed = 1111 #, help='Random seed (default: 1111)')
dilation_coefficient = 6 #, help='Dilation coefficient, recommended to be equal to kernel size (default: 4)')
 #, help="Significance number stating when an increase in loss is significant enough to label a potential cause as true (validated) cause. See paper for more details (default: 0.8)")

def runTCDF(data, hidden_layers, learning_rate, epochs, significance):
    """Loops through all variables in a dataset and return the discovered causes, time delays, losses, attention scores and variable names."""
    df_data = pd.DataFrame(data)

    allcauses = dict()
    alldelays = dict()
    allreallosses=dict()
    allscores=dict()

    columns = list(df_data)
    for c in columns:
        idx = df_data.columns.get_loc(c)
        causes, causeswithdelay, realloss, scores = TCDF.findcauses(c, cuda=cuda, epochs=epochs, 
        kernel_size=kernel_size, layers=hidden_layers+1, log_interval=log_interval, 
        lr=learning_rate, optimizername=optimizer,
        seed=seed, dilation_c=dilation_coefficient, significance=significance, data=df_data, verbose=False)

        allscores[idx]=scores
        allcauses[idx]=causes
        alldelays.update(causeswithdelay)
        allreallosses[idx]=realloss

    return allcauses, alldelays, allreallosses, allscores, columns


# Your method must be called 'my_method'
# Describe all parameters (except for 'data') in the method registration on CauseMe
def my_method(data, hidden_layers = 0, learning_rate = 0.01, epochs = 1000, significance = 0.8):

    # Input data is of shape (time, variables)
    T, N = data.shape

    # Standardize data  --> TODO: Not needed here?
    #data -= data.mean(axis=0)
    #data /= data.std(axis=0)
    
    allcauses, alldelays, allreallosses, allscores, columns = runTCDF(data, hidden_layers, learning_rate, epochs, significance)
    #return allcauses, alldelays, allreallosses, allscores, columns
    
    #########

    # CauseMe requires to upload a score matrix and
    # optionally a matrix of p-values and time lags where
    # the links occur

    # In val_matrix an entry [i, j] denotes the score for the link i --> j and
    # must be a non-negative real number with higher values denoting a higher
    # confidence for a link.
    # Fitting a VAR model results in several lagged coefficients for a
    # dependency of j on i.
    # Here we pick the absolute value of the coefficient corresponding to the
    # lag with the smallest p-value.
    val_matrix = np.zeros((N, N), dtype='float32')

    # Matrix of p-values
    p_matrix = np.ones((N, N), dtype='float32')

    # Matrix of time lags
    lag_matrix = np.zeros((N, N), dtype='uint8')

    for cause, lag in alldelays.items():
        i, j = cause
        val_matrix[i, j] = 1
        p_matrix[i, j] = 0
        lag_matrix[i, j] = lag

    return val_matrix, p_matrix, lag_matrix