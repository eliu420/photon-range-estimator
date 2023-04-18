
class Range_est():

    # initial_SOC = 0
    # initial_distance = 0
    # initial_time = 0

    # current_SOC = 0
    # current_distance = 0
    # current_time = 0

    # batt_cap = 0

    def __init__(self):

        if self.data['state_run']==1:
            initial_SOC = self.data['soc']
            initial_distance = self.data['tripDistance']
            initial_time = self.data['time']

        elif self.data['state_run'] != 1:       # need to fix dependant on current condition
            current_SOC = self.data['soc']
            current_distance = self.data['tripDistance']
            current_time = self.data['time']
        
        batt_cap = self.data['soh'] * 63
        energy_used = self.data['energyUsed']
        trip_mins = self.data['tripDuration']

    
    def overall_avg(data):
        """This function is based on an overall average of all the data in the trip.
        Takes in a dataframe from the vessel and the capacity of the battery."""

        batt = energyRemaining/batt_cap
        total_batt_consumed = energy_used/batt_cap
        total_dist_traveled = current_distance
        total_time_traveled = trip_mins * 60    # mins -> seconds

        # batt = self.data[]
        avg_consumption = total_batt_consumed/(total_time_traveled/3600)       #kWh/hr
        time_remaining = batt/avg_consumption                                          #hr
        # dist_remaining = time_remaining*current_data['Speed kts']                      #nm

        # return dist_remaining 

    # def rolling_avg(data, batt_cap, N):
    #     """This function is based on a rolling average consumption rate of N data points.
    #     Any consumption rates that are not valid, or within the first N data points of the run,
    #     will default to using the stored average consumption rate."""

    #     dist_list = []

    #     cached_avg = data_files.file_summary.iloc[run-1]['Average Consumption (kWh/nm)']       # need a cached average value to default to 
    #     for i in range(len(data)):
    #         batt = data['SOC 1 %'].iloc[i]*batt_cap/100
    #         roll_batt_consumed = (data['SOC 1 %'].iloc[i-N] - data['SOC 1 %'].iloc[i])*batt_cap/100          #kWh
    #         roll_dist_traveled = (data['Distance nm'].iloc[i] - data['Distance nm'].iloc[i-N])                  #nm
    #         roll_consumption = roll_batt_consumed/roll_dist_traveled                                            #kWh/nm
            
    #         if i < N or roll_consumption==0:
    #             dist_remaining = batt/cached_avg      # This will need to change because we won't know the average with real-time data
    #             print('%d Batt: %.1f | Consumption Rate: %.2f kWh/nm | Dist Remaining %.1f nm' % (i, batt, cached_avg, dist_remaining), end=' \r')
    #             # time.sleep(0.001)
    #         else:
    #             dist_remaining = batt/roll_consumption   #nm
    #             print('%d Batt: %.1f | Consumption Rate: %.2f kWh/nm | Dist Remaining: %.2f nm' % (i, batt, roll_consumption, dist_remaining), end=' \r')
    #             # time.sleep(.001)

    #         dist_list.append(dist_remaining)

    #     return dist_list
