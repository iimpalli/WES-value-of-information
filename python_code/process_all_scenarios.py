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
scen_list = ["PUT SCENARIOS HERE"]

with open(path_to_log, "w") as log:
    for curr_scen in scen_list:
        run_scenario(all_scenarios[0], scenario_name = scen_name)
        test_analysis(scenario_name = curr_scen)
