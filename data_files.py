import pandas as pd
import sys

file_dict = {
    'L230212.CSV': [[4800,8100]],
    'L230214.CSV': [[4800,6900], [7500,8900], [15600,18500]], #[21700,69000]],
    'L230215.CSV': [[3655,5600], [14000,16800], [22000,26000], [27350,30000]],
    'L230216.CSV': [[8000,11800], [13600, 15300], [16000, 19700], [20100,21500], [23400,25300], [31300,33000], [94000,98500]], #[600,3200], [29400,30700],
    'L230217.CSV': [[350,2400], [6300, 8500], [10400,14600]],
    'L230218.CSV': [[1200, 2700], [10500, 17500]],
    'L230219.CSV': [[9900,13950]],
    'L230303.CSV': [[2842,5900]],
    # 'L230306.CSV': [[16000,38500], [41000,62300]],
    'L230307.CSV': [[3000,5800], [6300,8800]],
    'L230331_1.csv': [[32500,35000], [47000,49000]],
    # 'L230403_1.csv': [[0,-1]],
    'L230413.CSV': [[5600, 6150]],
    'L230414.CSV': [[300, 3300]],
    'L230418.CSV': [[200, 2500]],
    'L230508.csv': [[0, 1850]]
    }

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

runs_dict = {}
keep = ['Date', 'Time', 'Speed m/s', 'Distance km', 'RPM 1',
        'Pack Current 1 A', 'Pack Voltage 1 V', 'SOC 1 %']

cnt = 0
# Loop through files and load data
for file in file_dict.keys():
    df = pd.read_csv("data/"+file)
    df = df[keep]
    
    # Loop through indices in each file and make each run a dataframe
    for ind in file_dict[file]:
        cnt+=1
        run = 'Run %d' % (cnt)
        runs_dict[run] = df[ind[0]:ind[1]]

        # Format columns appropriately
        runs_dict[run]['Time'] = pd.to_datetime(runs_dict[run]['Time'], format="%H:%M:%S")
        for col in df.columns[2:]:
            runs_dict[run][col] = pd.to_numeric(runs_dict[run][col])
