This folder contains all Python code needed to replicate the results of
"Optimal sampling frequency and site selection for wastewater and environmental surveillance
 of infectious pathogens: a value of information approach" by Impalli et al. A rough usage guide is as follows.

 Parameter values to alter the behavior of the simulation and set the scenarios to simulate are stored in
 important_parameters.py. To run the resulting scenarios, simply run process_all_scenarios.py. This file
 imports the code to run uninterrupted epidemics (while marking possible detection points) from
 create_numerical_simulations.py and to analyze all possible two-patch testing strategies from
 testing_analysis.py. The code has also been generalized to function with n patches.

 To recreate the figures used in the paper, see the accompanying R code. To prepare data to be
 processed in R, run postprocess_for_R.py.
