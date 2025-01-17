import numpy as np
from scipy.integrate import odeint
from scipy.linalg import expm
import os
from important_parameters import (num_sims, poisson_rates,
                                  tot_poisson, patch_sizes, final_day, num_WES_samples,
                                  possible_testing as possible_test_days)

# The code in this file is responsible for generating the simulations of uninterrupted epidemics.
# It also generates "potential detections" at each timestep, based on the current number of infected
# individuals in each patch. These are checked on the actual testing days, as carried out in
# testing_analysis.py. Results are saved to the current working directory and labeled with the
# precise growth matrix used.

def run_scenario(A):
    # extract elements of matrix in order to label resulting files
    r1 = A[0,0]
    r2 = A[1,1]
    eta_21 = A[0,1]
    eta_12 = A[1,0]

    # used to solve linear ODE, can be replaced with exact solution via scipy's expm
    def ode_rhs(y,t):
        return np.matmul(A,np.array(y))

    # probability disease arrives in a given patch
    patch_probs = poisson_rates / tot_poisson
    bernoulli_success = patch_probs[1]  # conduct Bernoulli trial. If successful, patch 1. If fail, patch 0

    # generate initial conditions, numpy uses scale not rate parameter: scale = 1/rate
    arrival_times = np.random.exponential(scale=1/tot_poisson, size=num_sims)
    arrival_patches = np.random.binomial(size=num_sims, n=1, p=bernoulli_success)

    # possible times to carry out testing, every quarter day since highest frequency in paper is 4/day
    possible_tests = np.linspace(0,final_day, 4*final_day+1)  # so that quarter days are included

    # to hold key results
    sim_results = np.zeros((num_sims, len(possible_tests), 2))  # hold simulations for all possible days, default values zero
    pop_fractions = np.zeros((num_sims, len(possible_tests), 2)) # fraction of patch infected, for disease detection
    disease_detected = np.zeros((num_sims, len(possible_tests), 2)) # stores "potential detections"

    # generate comparison random numbers, on a 1 per sim per patch per WES sample basis
    detection_rands = np.random.uniform(size=(num_sims, len(possible_tests), 2, num_WES_samples))

    print("Preliminaries completed, running simulations")

    for i in range(0, num_sims):
        ith_arrival = arrival_times[i]
        # only simulate days after the arrival of the disease
        viable_indices = (possible_tests >= ith_arrival)
        viable_days = possible_tests[viable_indices]
        # set initial condition for ODE based on chosen patch
        if arrival_patches[i] == 0:
            init_cond = np.array([1,0])
        else:
            init_cond = np.array([0,1])

        # fill out remainder of days with solution to ODE
        sim_results[i,viable_indices,:] = odeint(ode_rhs, init_cond, viable_days-ith_arrival)
        # compute fractions, let get bigger than 1 if needed. Simply guarantees detection, as required
        pop_fractions[i,:,0] = sim_results[i,:,0]/patch_sizes[0]
        pop_fractions[i,:,1] = sim_results[i,:,1]/patch_sizes[1]

        # conduct 10 samples, if any of them find disease treat as detection
        for k in range(0, num_WES_samples):
            disease_detected[i,:,:] = np.maximum((pop_fractions[i,:,:] > detection_rands[i,:,:,k]),disease_detected[i,:,:])


        # progress report
        if i % 100 == 0:
            print(f"Completed {i} ODE solutions for scenario [[{r1},{eta_21}],[{eta_12},{r2}]]")


    # names for storing results
    foldername = f"simulation_results_[[{r1},{eta_21}],[{eta_12},{r2}]]"
    cwd = os.getcwd()
    save_to = os.path.join(cwd, foldername)
    # if re-running analysis, check to see if directory already exists. Will overwrite previous results
    if not os.path.exists(save_to):
        os.makedirs(save_to)

    # save results
    np.save(os.path.join(save_to, "pop_fractions"), pop_fractions)
    np.save(os.path.join(save_to, "sim_results"), sim_results)
    np.save(os.path.join(save_to, "disease_detected"), disease_detected)

if __name__ == "__main__":
    # you can put code here if you want to run this file independently. The authors imported
    # the function above into another script to run the full analysis without stopping
    pass