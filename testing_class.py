import pandas as pd
import matplotlib as plt
import math
import sys
import time
from data_files import runs_dict
from range_estimator import range_est


class testing():

    def __init__(self):
        """Replicate relevant portions of the nmea2000 server dictionary"""

        self.battery = 58
        self.data = {
            'sog': 0,               # Knot, COG SOG Rapid Update
            'time': "12:34 PM",     # GNSS Position Data
            'power': 0.0,           # kW, calculated
            'tripDistance': 0.0,    # miles
            'soc': 0,               # %, DC Detailed Status
            'energyUsed': 0.0,      # kWh
            'totalDistance': 0,     # miles
            'minsRemaining': 0,     # mins, DC Detailed Status
            'tripDuration': 0,      # mins
            'packVoltage': 0,       # V, DC Voltage Current
            'packCurrent': 0.0,     # A, DC Voltage Current
            'rangeRemaining': 0
            }
        

    def add_variables(self, df):
        """Add calculated variables to testing DataFrame which show up in NMEA Server but aren't in CSV files"""
        
        df['Time'] = pd.to_datetime(df['Time'], format="%H:%M:%S")
        df['tripDistance'] = ''
        df['tripDuration'] = ''
        df['energyUsed'] = ''
        df['energyAvailable'] = ''

        for i in range(len(df)):
            df['tripDistance'].iloc[i] = (df['Distance km'].iloc[i] - df['Distance km'].iloc[0])*.539957        # nm
            df['tripDuration'].iloc[i] = (df['Time'].iloc[i] - df['Time'].iloc[0]).seconds                      # sec
            df['energyUsed'].iloc[i] = (df['SOC 1 %'].iloc[0] - df['SOC 1 %'].iloc[i])*self.battery/100         # kWh
            df['energyAvailable'].iloc[i] = df['SOC 1 %'].iloc[i]*self.battery/100                              # kWh
        return df


    def parse_csv(self, df):
        """Interpret DataFrame values as class variables to replicate NMEA Server"""

        self.data['sog'] = df['Speed m/s']*1.94384              # knots
        self.data['time'] = df['Time']                          # datetime
        self.data['totalDistance'] = df['Distance km']*0.539957 # nm
        self.data['soc'] = df['SOC 1 %']                        # %
        self.data['packVoltage'] = df['Pack Voltage 1 V']*10    # V
        self.data['packCurrent'] = df['Pack Current 1 A']       # A

        '''Missing Variables'''
        self.data['tripDistance'] = df['tripDistance']          # nm; manually added in test loop
        self.data['energyUsed'] = df['energyUsed']              # kWh; manually added in test loop
        self.data['energyAvailable'] = df['energyAvailable']    # kWh; manually added in test loop
        self.data['tripDuration'] = df['tripDuration']          # min; manually added in test loop

        '''Calculated Variables'''
        self.data['power'] = self.data['packVoltage']*self.data['packCurrent']/1000   # kW    

        return self.data
    

    def test_accuracy(self, df, range_list, interval=500):
        """Add list of calculated range estimates to the dataframe and compare them with
        tripDistance between two points, A and B. Point B is always the last row of the data. 
        The interval (in seconds) defines how often point A is re-defined and values are compared."""

        df['Dist Prediction (nm)'] = range_list
        N = range(interval, len(df), interval)
        error_list = []
        for n in N:
            pred = df['Dist Prediction (nm)'].iloc[n] - df['Dist Prediction (nm)'].iloc[-1]     # predicted distance remaining at n minus the prediction at the end of trip
            dist = df['tripDistance'].iloc[-1] - df['tripDistance'].iloc[n]                     # actual distance traveled since n
            error = abs(pred - dist)
            error_list.append(error)
        run_error = (sum(error_list)/len(error_list))                                           # average error for whole trip
        
        return run_error, error_list


## This statement avoids annoying errors popping up all the time
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


"""Example"""
# '''Import chosen Data from file manager'''
# df = testing().add_variables(runs_dict['Run 10'])

# '''Create algorithm instance'''
# range_estimator = range_est(58, 2.5, 0.3, 0, 0, 0)

# range_list = []
# """Test Loop"""
# for i in range(len(df)):
#     dataStream = testing().parse_csv(df.iloc[i])

#     range_estimator.overall_avg(dataStream)
#     # range_estimator.overall_time_avg(dataStream)
#     # range_estimator.rolling_avg(dataStream)
    
#     print('Battery Remaining = %.1f percent | Range Remaining = %.1f nm' % (dataStream['soc'], range_estimator.range_remaining))
#     time.sleep(.005)
#     range_list.append(range_estimator.range_remaining)

# error, errors_list = testing().test_accuracy(df, range_list)
# print('Run Error = ', error)