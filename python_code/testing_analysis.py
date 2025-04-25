import numpy as np
from scipy.integrate import odeint
from itertools import product
import os
from important_parameters import final_day, patch_sizes, possible_testing, possible_tests

# This file handles the computation of the sample means discussed in the paper. It reloads the simulation
# results and overlays every possible testing protocol. For example, if possible testing periods are
# [1,2], then this file computes the expected number of infected in both patches and time of detection for
# (1,1), (1,2), (2,1), (2,2). Results are then saved for analysis in the cost function.

def test_analysis(scenario_name="default"):
    cwd = os.getcwd()
    foldername = f"{scenario_name}"
    load_from = os.path.join(cwd, foldername)

    sim_results = np.load(os.path.join(load_from,"sim_results.npy"))
    disease_detected = np.load(os.path.join(load_from,"disease_detected.npy"))
    # number and length of simulations automatically detected, could move to important_parameters.py
    num_sims = np.shape(sim_results)[0]
    length_sim = np.shape(sim_results)[1]
    num_patches = len(patch_sizes)

    # Recreate grid consisting of every quarter day in simulations
    testing_days = possible_tests
    # how many combinations of testing frequencies are there
    all_strategies = list(product(possible_testing, repeat=num_patches))
    strategy_combinations = len(all_strategies)
    # Finds index where no testing is done, if present
    for i in range(0, strategy_combinations):
        curr_strat = all_strategies[i]
        if min(curr_strat) == np.inf:
            no_test_index = i
            break

    # accumulator variables for quantities of interest
    mean_pops = np.zeros((strategy_combinations, num_patches))
    mean_detection_time = np.zeros(strategy_combinations)
    mean_false_pos = np.zeros(strategy_combinations)

    for i in range(0, num_sims):
        # retrieves results from one simulation
        one_sim = sim_results[i,:,:]
        one_dd = disease_detected[i,:,:]

        # creates a useful variable to check for false positives, if no cases at detection then it is a false positive
        total_cases = np.sum(one_sim, axis=1)
        cases_present = total_cases > 0

        # determines if the disease has been detected yet for a given strategy pair.
        # If not, must check until it is found
        found_yet = np.zeros(strategy_combinations, dtype=bool)

        # we automatically set no testing in either patch to max time and max population
        # this way, there is some hope of breaking off early, but not in uncoupled patches
        try:
            found_yet[no_test_index] = True
            mean_pops[no_test_index, :] += patch_sizes  # clamps to population size
            mean_detection_time[no_test_index] += final_day
        except:
            print("No non-testing scenarios")

        for j in range(0, length_sim):
            if np.sum(found_yet) == strategy_combinations:
                break  # every strategy has found the disease in current simulation, move on to the next
            current_time = testing_days[j]
            for k in range(0, strategy_combinations):
                if not found_yet[k]: # only search strategies without detections, no testing automatically considered "detected"
                    valid_day = current_time % np.array(all_strategies[k]) == 0 # check whether any patches should be tested
                    valid_and_detected = np.sum(np.logical_and(valid_day, one_dd[j, :])) > 0  # true if any patches testing today see a detection
                    if valid_and_detected:
                        found_yet[k] = True
                        mean_pops[k, :] += np.minimum(one_sim[j,:],patch_sizes)  # clamps to population size
                        mean_detection_time[k] += current_time
                        if not cases_present[j]:  # a detection has occurred without cases => false positive
                            mean_false_pos[k] += 1
                    elif j == length_sim-1:
                        # we have reached the end of the sim, detection has failed
                        found_yet[k] = True
                        mean_pops[k, :] += patch_sizes  # clamps to population size
                        mean_detection_time[k] += final_day

        if i % 100 == 0:
            print(f"Completed analysis of {i} simulations for"
                  f" testing strategies for scenario {scenario_name}")


    # when done accumulating results, divide by num_sims to compute sample mean
    mean_pops = mean_pops/num_sims
    mean_detection_time = mean_detection_time/num_sims
    mean_false_pos = mean_false_pos/num_sims

    # save results
    np.save(os.path.join(load_from, "mean_pops"), mean_pops)
    np.save(os.path.join(load_from, "mean_detection_time"), mean_detection_time)
    np.save(os.path.join(load_from, "mean_false_pos"), mean_false_pos)

if __name__ == "__main__":
    # you can put code here if you want to run this file independently. The authors imported
    # the function above into another script to run the full analysis without stopping
    pass
