# apero-mock

mock apero codes for CANFAR test


## processing.py

Run this to generate an "apero-run" file with the list of "recipes" to run
in the order they should be run. Note that each group must be run in this 
order but all runs in a group can be run independently and in parrellel.

Note this is a fake processing script - the recipe names, arguments, number
of runs per group and number of groups will differ for the real apero-processing
code.

## recipe1.py and recipe2.py

These are fake recipes and represent programs to be run. A individual run
in a group in apero-run.txt will run either recipe1.py or recipe2.py with
two arguments (a group number and a run number)
