import numpy as np
from scipy.integrate import odeint
import os
from important_parameters import final_day, patch_sizes, possible_testing

# This file handles the computation of the sample means discussed in the paper. It reloads the simulation
# results and overlays every possible testing protocol. For example, if possible testing periods are
# [1,2], then this file computes the expected number of infected in both patches and time of detection for
# (1,1), (1,2), (2,1), (2,2). Results are then saved for analysis in the cost function.

def test_analysis(A):
    # find associated results by generating filename used in process_all_scenarios
    r1 = A[0, 0]
    r2 = A[1, 1]
    eta_21 = A[0, 1]
    eta_12 = A[1, 0]

    cwd = os.getcwd()
    foldername = f"simulation_testing_results_[[{r1},{eta_21}],[{eta_12},{r2}]]"
    load_from = os.path.join(cwd, foldername)

    sim_results = np.load(os.path.join(load_from,"sim_results.npy"))
    disease_detected = np.load(os.path.join(load_from,"disease_detected.npy"))
    # number and length of simulations automatically detected, could move to important_parameters.py
    num_sims = np.shape(sim_results)[0]
    length_sim = np.shape(sim_results)[1]

    # Recreate grid consisting of every quarter day in simulations
    testing_days = np.linspace(0,final_day, 4*final_day+1)
    # Assumes test_period = infinity is an option and determines which it is
    no_test_index = possible_testing.argmax()
    number_strategies = len(possible_testing)

    # accumulator variables for quantities of interest
    mean_pop_one = np.zeros((number_strategies, number_strategies))
    mean_pop_two = np.zeros((number_strategies, number_strategies))
    mean_detection_time = np.zeros((number_strategies, number_strategies))

    for i in range(0, num_sims):
        # retrieves results from one simulation
        one_sim = sim_results[i,:,:]
        one_dd = disease_detected[i,:,:]

        # determines if the disease has been detected yet for a given strategy pair.
        # If not, must check until it is found
        found_yet = np.zeros((number_strategies, number_strategies), dtype=bool)

        # we automatically set no testing in either patch to max time and max population
        # this way, there is some hope of breaking off early, but not in uncoupled patches
        found_yet[no_test_index, no_test_index] = True
        mean_pop_one[no_test_index, no_test_index] += patch_sizes[0]  # clamps to population size
        mean_pop_two[no_test_index, no_test_index] += patch_sizes[1]  # clamps to population size
        mean_detection_time[no_test_index, no_test_index] += final_day

        for j in range(0, length_sim):
            #  diagnostic output, can be removed
            if i % 100 == 0:
                try:
                    print(f"On time {testing_days[j - 1]} completed {np.sum(found_yet)} strategies")
                except:
                    pass
            if np.sum(found_yet) == number_strategies ** 2:
                break  # every strategy has found the disease in current simulation, move on to the next
            current_time = testing_days[j]
            # loop over all testing protocols, and if they haven't found the disease, check if
            # they apply to the current time of the simulation. If so, check for disease.
            for m in range(0, number_strategies):
                for n in range(0, number_strategies):
                    # double-infinite testing handled separately
                    if not ((m==no_test_index) and (n==no_test_index)):
                        patch_one_candidate = (current_time % possible_testing[m] == 0)
                        patch_two_candidate = (current_time % possible_testing[n] == 0)
                        if (not found_yet[m,n]) and ((patch_one_candidate and one_dd[j,0]) or (patch_two_candidate and one_dd[j,1])):
                            found_yet[m,n] = True
                            mean_pop_one[m,n] += min(one_sim[j,0], patch_sizes[0])  # clamps to population size
                            mean_pop_two[m,n] += min(one_sim[j,1], patch_sizes[1])  # clamps to population size
                            mean_detection_time[m,n] += current_time
                        elif (not found_yet[m,n]) and j == length_sim-1:
                            # we have reached end of sim, detection has failed
                            found_yet[m,n] = True
                            mean_pop_one[m,n] += patch_sizes[0]  # clamps to population size
                            mean_pop_two[m,n] += patch_sizes[1]  # clamps to population size
                            mean_detection_time[m,n] += final_day

        if i % 100 == 0:
            print(f"Completed analysis of {i} simulations for"
                  f" testing strategies for scenario [[{r1},{eta_21}],[{eta_12},{r2}]]")


    # when done accumulating results, divide by num_sims to compute sample mean
    mean_pop_one = mean_pop_one/num_sims
    mean_pop_two = mean_pop_two/num_sims
    mean_detection_time = mean_detection_time/num_sims

    # save results
    np.save(os.path.join(load_from, "mean_pop_one"), mean_pop_one)
    np.save(os.path.join(load_from, "mean_pop_two"), mean_pop_two)
    np.save(os.path.join(load_from, "mean_detection_time"), mean_detection_time)

if __name__ == "__main__":
    # you can put code here if you want to run this file independently. The authors imported
    # the function above into another script to run the full analysis without stopping
    pass
