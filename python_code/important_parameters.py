import numpy as np

# This file serves as a sort of configuration file for the project, storing important parameters that
# each of the key scripts then imports. For future work, a more standard approach such as a YAML file
# may be used. Ensure that this file is in the same working directory as the scripts used in the analysis.

# how many simulations in full run
num_sims = 10**5  # 100,000 simulations

# quantities defining the arrival of the disease, poisson_rates are the Poisson rate parameters for the
# arrival times in each patch. Their sum also appears throughout the code.
poisson_rates = np.array([0.15, 0.15])
tot_poisson = np.sum(poisson_rates)

# set patch populations
patch_sizes = np.array([5000.0, 5000.0])

# max days in experiments and list of test periods, decrease number of periods or final_day for
# faster simulations.
final_day = 100
possible_testing = np.array([0.25, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, np.inf])

# number of WES samples per day, decrease for faster simulations
num_WES_samples = 10

# define all scenarios to be run. Examples from the work discussed in the paper are given below.
# To include a scenario, uncomment it and place it in all_scenarios, or define your own.
# A1 = np.array([[0.4,0.0],[0.0,0.2]])
# A2 = np.array([[0.4,0.001],[0.001,0.2]])
# A3 = np.array([[0.4,0.003],[0.003,0.2]])
# A4 = np.array([[0.4,0.005],[0.005,0.2]])
# A5 = np.array([[0.4,0.01],[0.01,0.2]])
#
# A6 = np.array([[0.2,0.0],[0.0,0.2]])
# A7 = np.array([[0.2,0.001],[0.001,0.2]])
# A8 = np.array([[0.2,0.003],[0.003,0.2]])
# A9 = np.array([[0.2,0.005],[0.005,0.2]])
# A10 = np.array([[0.2,0.01],[0.01,0.2]])
#
# A11 = np.array([[0.4,0.05],[0.05,0.2]])
# A12 = np.array([[0.4,0.1],[0.1,0.2]])
# A13 = np.array([[0.2,0.15],[0.15,0.2]])

all_scenarios = []

# name of log to output readouts for running the full analysis
logfile = "log_results.txt"
