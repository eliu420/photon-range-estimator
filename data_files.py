import pandas as pd

file_dict = {
    'L230212.CSV': [[4800,8100]],
    'L230214.CSV': [[5000,7163], [7165,8950], [15500,18700], [21700,69950]],
    'L230215.CSV': [[3655,5600], [14000,16800], [22000,26000], [27350,30000]],
    'L230216.CSV': [[600,3200], [4540,19700], [20100,21500], [23400,25300], [29400,30700], [31300,33000], [94000,98500]],
    'L230217.CSV': [[300,2400], [2700,9300], [9900,14600]],
    'L230218.CSV': [[500,21500]],
    'L230219.CSV': [[9900,13950]],
    'L230303.CSV': [[2842,5900]],
    'L230306.CSV': [[16000,38500], [41000,62300]],
    'L230307.CSV': [[0,5800], [6300,9000]],
    'L230331_1.csv': [[32500,35000], [47000,49000]],
    'L230403_1.csv': [[0,-1]]
}

batt_cap = 63       #kWh

runs_dict = {}
file_summary = pd.DataFrame({
    'File': [],
    'Run': [],
    'Time (min)': [],
    'Max Speed (kts)': [],
    'Avg Speed (kts)': [],
    'Battery Expended (%)': [],
    'Distance Traveled (nm)': [],
    'Average Consumption (kWh/nm)': []
})
cnt = 0
for file in file_dict.keys():
    df = pd.read_csv("data/"+file)
    for ind in file_dict[file]:
        cnt+=1
        run = 'Run %d' % (cnt)
        runs_dict[run] = df[ind[0]:ind[1]]

        for col in df.columns[2:]:
            runs_dict[run][col] = pd.to_numeric(runs_dict[run][col])
        runs_dict[run]['Time'] = pd.to_datetime(runs_dict[run]['Time'], format="%H:%M:%S")

        runs_dict[run]['Pack Voltage 1 V'] = runs_dict[run]['Pack Voltage 1 V']*10
        runs_dict[run]['Power 1 kW'] = runs_dict[run]['Pack Current 1 A']*runs_dict[run]['Pack Voltage 1 V']/1000
        runs_dict[run]['Speed kts'] = runs_dict[run]['Speed m/s']*1.944
        runs_dict[run]['Distance nm'] = runs_dict[run]['Distance km']*0.539957
        # runs_dict[run]['SOC Interpolated'] = 
        # runs_dict[run]['Coulombs Remain'] = runs_dict[run]['SOC 1 %']*batt_cap/runs_dict[run]['Pack Voltage 1 V']*1000*3600

        time_elapsed = runs_dict[run]['Time'].iloc[-1] - runs_dict[run]['Time'].iloc[0]
        speed_max = runs_dict[run]['Speed kts'].max()
        speed_avg = runs_dict[run]['Speed kts'].mean()
        battery_expended = runs_dict[run]['SOC 1 %'].iloc[0] - runs_dict[run]['SOC 1 %'].iloc[-1]
        distance_traveled = runs_dict[run]['Distance nm'].iloc[-1] - runs_dict[run]['Distance nm'].iloc[0]
        avg_consumption = (battery_expended*63/100)/distance_traveled

        file_summary.loc[len(file_summary.index)] = [
            file, 
            run, 
            time_elapsed.seconds/60,
            speed_max,
            speed_avg,
            battery_expended,
            distance_traveled,
            avg_consumption
            ]