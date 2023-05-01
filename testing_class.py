import pandas as pd
import matplotlib as plot
from algorithm_class import range_est


class testing():

    def __init__(self):
        self.data = {
            'sog': 0,               # Knot, COG SOG Rapid Update
            'rpm': 0,               # RPM, Engine Parameters Rapid Update
            'date': "12:34 PM",     # GNSS Position Data
            'time': "12:34 PM",     # GNSS Position Data
            'cog': 0,               # Deg, COG SOG Rapid Update
            'heading': "N",         # calculated
            'numFaults': 0,         # TODO
            'faults': "",           # TODO
            'power': 0.0,           # kW, calculated
            'tripDistance': 0.0,    # miles
            'soc': 0,               # %, DC Detailed Status
            'energyUsed': 0.0,      # kWh
            'battCycles': 0,        # stored locally
            'motorTemp': 0,         # degC, Engine Parameters Dynamic
            'totalDistance': 0,     # miles
            'minsRemaining': 0,     # mins, DC Detailed Status
            'tripDuration': 0,      # mins
            'motorTorquePct': 0,    # %, Engine Parameters Dynamic
            'packVoltage': 0,       # V, DC Voltage Current
            'packCurrent': 0.0,     # A, DC Voltage Current
            'packTemp': 0,          # degC, Battery Status
            'soh': 0,               # %, DC Detailed Status
            'totalMotorHours': 0.0, # hours motor rpm > 0
            'motorVoltage': 0,      # V, Engine Parameters Dynamic (alternator potential /10)
            'gear': "Unknown",      # Neutral, Forward, Reverse
            'motorEnabled': 0,      # 0: disabled, 1: enabled
            'nmea2000_timeout': 0,  # 0: NMEA2000 data received (EV), 1: timeout
            'state_sleep': 0,
            'state_acc': 0,
            'state_ign': 0,
            'state_run': 0,
            'state_charge': 0
            }


    def add_variables(self, df):
        """Add calculated variables to testing DataFrame which show up in NMEA Server but aren't in CSV files"""
        
        df['Time'] = pd.to_datetime(df['Time'], format="%H:%M:%S")
        df['tripDistance'] = ''
        df['tripDuration'] = ''
        df['energyUsed'] = ''

        for i in range(len(df)):
            df['tripDistance'].iloc[i] = (df['Distance km'].iloc[i] - df['Distance km'].iloc[0])*.539957    # nautical miles
            df['tripDuration'].iloc[i] = (df['Time'].iloc[i] - df['Time'].iloc[0]).seconds/60               # min
            df['energyUsed'].iloc[i] = (df['SOC 1 %'].iloc[0] - df['SOC 1 %'].iloc[i])*58/100               # kWh
        return df


    def parse_csv(self, df):
        """Interpret DataFrame values as data class values to replicate NMEA Server"""

        self.data['sog'] = df['Speed m/s']*1.94384          # knots
        self.data['time'] = df['Time']
        self.data['totalDistance'] = df['Distance km']*0.539957
        self.data['soc'] = df['SOC 1 %']
        self.data['packVoltage'] = df['Pack Voltage 1 V']*10
        self.data['packCurrent'] = df['Pack Current 1 A']

        '''Missing Variables'''
        self.data['tripDistance'] = df['tripDistance']      # manually added in test loop
        self.data['energyUsed'] = df['energyUsed']          # manually added in test loop
        self.data['tripDuration'] = df['tripDuration']      # manually added in test loop

        '''Calculated Columns'''
        self.data['power'] = self.data['packVoltage'] * self.data['packCurrent'] / 1000.0   # kW    

        return self.data
    
    
test_instance = testing()
file_path = 'data/L230414.CSV'

#skiprows helps us read certain sections of a run file.
df = pd.read_csv(file_path) #, skiprows= lambda x : x not in range(rows_to_read [0][0], rows_to_read[0][1]+1))
df = test_instance.add_variables(df[300:3300])      # Add in variables like tripDistance and energyUsed on filtered dataset

for i in range(len(df)):
    data = test_instance.parse_csv(df.iloc[i])
    # avg_consumption, time_remaining, range_remaining = Range_est().overall_time_avg(data)
    avg_consumption, range_remaining = range_est(58).overall_dist_avg(data)

    print(range_remaining)

#and then we call the algorithm_class and give it data output from the testing,
#then we have output here in a plot to make sure it looks simlar to our notebook tests.



    