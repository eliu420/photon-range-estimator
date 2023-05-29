# photon-range-estimator
UW EE 497/498 Capstone Project
Developed by Ean Barnawell, Elliot Liu, Ryan Ostrander, Theo Reid

## Purpose
This algorithm estimates the range remaining on the battery of an marine electric vehicle given a data stream of values including state of charge (SOC), distance and time traveled, current and voltage. It is designed to be implemented into Photon Marine's onboard UX system based on data from the BMS. 

## Directory
Below is a summary of the important files in this repository and what their purpose is:

range_estimator.py is the output of this project to be implemented on the vessel. It is a class of different functions which includes multiple types of range algorithms attempted. Although the overall average proved to be most accurate, the others were kept in the class for transparency. 

data_files.py consolidates trip data that was previously recorded for analysis and shared by Photon. This file reads each .csv file that is located in the 'data' folder, filters out observed periods of non-operation, transforms it into a pandas DataFrame, and stores each trip in a dictionary labeled 'runs_dict' that can be imported and called upon from other files. 

testing_class.py is a class of functions which transform the rows of a DataFrame in 'runs_dict' into a stream of data which mimics output from the boat. By testing with this class, we could be confident that our algorithm would integrate onto the physical vessel. 

test_loop.ipynb is a jupyter notebook that was used throughout as a test platform for various development exercises. In its current form, it imports data_files, range_estimator, and testing_class and runs them in various ways to plot the results and compare them. 

## How to use
For an example of how to implement and test the algorithm, see the bottom of testing_class.py following the class definition. 

