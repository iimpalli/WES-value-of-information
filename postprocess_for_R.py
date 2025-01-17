import numpy as np
import pandas as pd
import os
from important_parameters import possible_testing, all_scenarios

# This code exists purely due to the division of labor of the authors. One author generated simulation results
# using this Python code, and all visualizations and the analysis of various asymmetries in the cost of
# testing and disease burden took place in R (see separate folder in this repository).

# plotting is done in terms of frequencies, not periods
possible_frequencies = 1.0/possible_testing
num_frequencies = len(possible_frequencies)

def numpy_to_csv(mean_detect_time, mean_pop_one, mean_pop_two, save_location):
    # this will be turned into a dataframe, then exported to a csv file
    row_wise_data = []
    # search through dataframes and collect data for each frequency pair
    for m in range(0, num_frequencies):
        for n in range(0, num_frequencies):
            # form of row determined by agreement between authors for ease of importation into R
            row = [possible_frequencies[m], possible_frequencies[n],
                   mean_pop_one[m,n], mean_pop_two[m,n], mean_detect_time[m,n]]
            row_wise_data.append(row)

    df = pd.DataFrame(row_wise_data, columns=["Freq1", "Freq2", "Patch1Size", "Patch2Size", "DetTime"])
    df.to_csv(save_location)

def process_folder(A, save_to):
    # find and load associated results
    r1 = A[0, 0]
    r2 = A[1, 1]
    eta_21 = A[0, 1]
    eta_12 = A[1, 0]

    cwd = os.getcwd()
    foldername = f"simulation_testing_results_[[{r1},{eta_21}],[{eta_12},{r2}]]"
    load_folder = os.path.join(cwd, foldername)

    mean_pop_one = np.load(os.path.join(load_folder,"mean_pop_one.npy"))
    mean_pop_two = np.load(os.path.join(load_folder, "mean_pop_two.npy"))
    mean_detection_time = np.load(os.path.join(load_folder, "mean_detection_time.npy"))

    # output to an R-friendly csv
    outfile = os.path.join(save_to, f"R_version_of_[[{r1},{eta_21}],[{eta_12},{r2}]].csv")
    numpy_to_csv(mean_detection_time, mean_pop_one, mean_pop_two, outfile)

if __name__ == "__main__":
    cwd = os.getcwd()
    # choose a folder for the outputs and fill it in where indicated
    save_to = os.path.join(cwd, "YOUR_FOLDER_HERE")
    if not os.path.exists(save_to):
        os.makedirs(save_to)

    # modification of scenarios takes place in important_parameters.py
    for A in all_scenarios:
        process_folder(A, save_to)