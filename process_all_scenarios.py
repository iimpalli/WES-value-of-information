import os
import numpy as np

from create_numerical_simulations import run_scenario
from testing_analysis import test_analysis
from important_parameters import all_scenarios, logfile

# This file imports the main body of code from the files testing_analysis.py and
# create_numerical_simulations.py to automate analysis of a predefined list of scenarios. Results are
# saved via the code in these other files, in the current working directory.

# set up logging file, save in current working directory
cwd = os.getcwd()
path_to_log = os.path.join(cwd, logfile)

with open(path_to_log, "w") as log:
    for A in all_scenarios:
        # extract to find relevant files, as previously
        r1 = A[0, 0]
        r2 = A[1, 1]
        eta_21 = A[0, 1]
        eta_12 = A[1, 0]

        log.write(f"Beginning work on scenario [[{r1},{eta_21}],[{eta_12},{r2}]]\n")
        run_scenario(A)
        log.write(f"Simulations generated for [[{r1},{eta_21}],[{eta_12},{r2}]]\n")
        test_analysis(A)
        log.write(f"Analysis of testing strategies on full sample for [[{r1},{eta_21}],[{eta_12},{r2}]] complete\n\n")
