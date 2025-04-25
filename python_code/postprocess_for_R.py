import numpy as np
import pandas as pd
import os
from itertools import product
from important_parameters import possible_testing, all_scenarios, num_patches

# This code exists purely due to the division of labor of the authors. One author generated simulation results
# using this Python code, and all visualizations and the analysis of various asymmetries in the cost of
# testing and disease burden took place in R (see separate folder in this repository).

# plotting is done in terms of frequencies, not periods
possible_frequencies = 1.0/possible_testing
num_frequencies = len(possible_frequencies)

# how many combinations of testing frequencies are there
all_strategies = list(product(possible_frequencies, repeat=num_patches))
strategy_combinations = len(all_strategies)

def numpy_to_csv(mean_detect_time, mean_pops, false_pos_perc, save_location):
    # this will be turned into a dataframe, then exported to a csv file
    row_wise_data = []
    # search through dataframes and collect data for each frequency pair
    for i in range(0, strategy_combinations):
        row = [all_strategies[i][0], all_strategies[i][1],
               mean_pops[i,0], mean_pops[i,1], mean_detect_time[i], false_pos_perc[i]]
        row_wise_data.append(row)

    df = pd.DataFrame(row_wise_data, columns=["Freq1", "Freq2", "Patch1Size", "Patch2Size", "DetTime","FalsePos%"])
    df.to_csv(save_location)

def process_folder(scenario_name, save_to):
    cwd = os.getcwd()
    load_folder = os.path.join(cwd, scenario_name)

    mean_pops = np.load(os.path.join(load_folder,"mean_pops.npy"))
    mean_detection_time = np.load(os.path.join(load_folder, "mean_detection_time.npy"))
    false_pos_perc = np.load(os.path.join(load_folder, "mean_false_pos.npy"))

    # output to an R-friendly csv
    outfile = os.path.join(save_to, scenario_name)
    numpy_to_csv(mean_detection_time, mean_pops, false_pos_perc, outfile)

if __name__ == "__main__":
    cwd = os.getcwd()
    # choose a folder for the outputs and fill it in where indicated
    save_to = os.path.join(cwd, "one_drive_outputs")
    if not os.path.exists(save_to):
        os.makedirs(save_to)

    scenario_list = ["PUT SCENARIO NAMES HERE"]
    for scenario_name in scenario_list:
        process_folder(scenario_name, save_to)
