import numpy as np
import random
from scipy.integrate import odeint
from scipy.linalg import expm
import os
from important_parameters import (num_sims, poisson_rates,
                                  tot_poisson, patch_sizes, final_day, num_WES_samples,
                                  possible_testing as possible_test_days, possible_tests,
                                  false_pos_rate, vote_thresh)

# The code in this file is responsible for generating the simulations of uninterrupted epidemics.
# It also generates "potential detections" at each timestep, based on the current number of infected
# individuals in each patch. These are checked on the actual testing days, as carried out in
# testing_analysis.py. Results are saved to the current working directory and labeled with the
# precise growth matrix used.

def run_scenario(A, scenario_name="default"):
    # used to solve linear ODE, can be replaced with exact solution via scipy's expm
    def ode_rhs(y,t):
        return np.matmul(A,np.array(y))

    # probability disease arrives in a given patch
    patch_probs = poisson_rates / tot_poisson
    num_patches = len(patch_probs)

    # generate initial conditions, numpy uses scale not rate parameter: scale = 1/rate
    arrival_times = np.random.exponential(scale=1/tot_poisson, size=num_sims)
    arrival_patches = np.zeros(num_sims)
    # generate actual realizations of multinomial trials, not just counts
    for i in range(0, num_sims):
        x = random.random()
        patch_result = 0
        prob_sum = patch_probs[0]
        while prob_sum < x:
            patch_result += 1
            prob_sum += patch_probs[patch_result]
        arrival_patches[i] = patch_result

    # to hold key results
    sim_results = np.zeros((num_sims, len(possible_tests), num_patches))  # hold simulations for all possible days, default values zero
    pop_fractions = np.zeros((num_sims, len(possible_tests), num_patches)) # fraction of patch infected, for disease detection
    disease_detected = np.zeros((num_sims, len(possible_tests), num_patches)) # stores "potential detections"

    # generate comparison random numbers, on a 1 per sim per patch per WES sample basis
    detection_rands = np.random.uniform(size=(num_sims, len(possible_tests), num_patches, num_WES_samples))

    # generate false positives
    false_positive_tests = np.random.uniform(size=(num_sims, len(possible_tests), num_patches, num_WES_samples)) < false_pos_rate

    print("Preliminaries completed, running simulations")

    for i in range(0, num_sims):
        ith_arrival = arrival_times[i]
        # only simulate days after the arrival of the disease
        viable_indices = (possible_tests >= ith_arrival)
        viable_days = possible_tests[viable_indices]
        # set initial condition for ODE based on chosen patch
        init_cond = np.zeros(num_patches)
        init_cond[int(arrival_patches[i])] = 1

        # fill out remainder of days with solution to ODE
        sim_results[i,viable_indices,:] = odeint(ode_rhs, init_cond, viable_days-ith_arrival)
        # compute fractions, let get bigger than 1 if needed. Simply guarantees detection, as required
        for k in range(0, num_patches):
            pop_fractions[i,:,k] = sim_results[i,:,k]/patch_sizes[k]

        # conduct 10 samples, if any of them find disease treat as detection
        for k in range(0, num_WES_samples):
            no_false_pos = (pop_fractions[i, :, :] > detection_rands[i, :, :, k])
            include_false_pos = np.maximum(false_positive_tests[i,:,:,k], no_false_pos)
            #disease_detected[i,:,:] = np.maximum(include_false_pos,disease_detected[i,:,:])
            disease_detected[i,:,:] += include_false_pos.astype(int) # change to ints so we accumulate votes
        # after accumulating all positive test results, transform entries to a Boolean
        # by comparing to a threshold. vote_thresh = 0 counts any detected disease
        disease_detected[i, :, :] = disease_detected[i,:,:] > vote_thresh

        # progress report
        if i % 100 == 0:
            print(f"Completed {i} ODE solutions for scenario {scenario_name}")


    # names for storing results
    foldername = f"{scenario_name}"
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
