
class Range_est():

    def __init__(self):
        self.data['sog'] = sog
        self.data['time'] = time 
        self.data['totalDistance'] = totalDistance
        self.data['soc'] = soc 
        self.data['packVoltage'] = packVoltage 
        self.data['packCurrent'] = packCurrent
        self.data['tripDistance'] = tripDistance
        self.data['energyUsed'] = energyUsed
        self.data['tripDuration'] = tripDuration
        self.data['power'] = power
        self.data['soh'] = soh

    
    def overall_avg(self):
        '''Distance consumption version'''
        # avg_consumption = energyUsed/tripDistance               #kWh/nm
        # range_remaining = (soc*58/100)/avg_consumption          #nautical miles

        '''Time consumption version'''
        avg_consumption = energyUsed/tripDuration                  # kWh/min
        time_remaining = soc*(58*soh)/100/avg_consumption          # min
        range_remaining = time_remaining*(sog/60)                  # nm

        return avg_consumption, time_remaining, range_remaining


    def rolling_avg(self, cached_avg, N_minutes):
        """This function updates the range based on the trip duration. 
        Range will be calculated based on cached_avg (cached average energy consumption) for the first N minutes of the trip.
        After N minutes, range will be calculated with the average consumption for the given trip."""

        batt = soc*(58*soh)/100                             
        roll_consumption = energyUsed/tripDistance          # kWh/nm
        range_remaining = 0                                 # nm

        if tripDuration < N_minutes or roll_consumption==0:
            range_remaining = batt/cached_avg      
        else:
            range_remaining = batt/roll_consumption   #nm

        return range_remaining
    
    # def rolling_avg(self, cached_avg, N):
    #     """This function is based on a rolling average consumption rate of N data points.
    #     Any consumption rates that are not valid, or within the first N data points of the run,
    #     will default to using the stored average consumption rate."""

    #     dist_list = []

    #     for i in range(len(data)):
    #         batt = soc.iloc[i]*(58*soh)/100
    #         roll_batt_consumed = (soc.iloc[i-N] - soc.iloc[i])*(58*soh)/100          #kWh
    #         roll_dist_traveled = (tripDistance.iloc[i] - tripDistance.iloc[i-N])     #nm
    #         roll_consumption = roll_batt_consumed/roll_dist_traveled                 #kWh/nm
            
    #         if i < N or roll_consumption==0:
    #             range_remaining = batt/cached_avg      # This will need to change because we won't know the average with real-time data
    #             # print('%d Batt: %.1f | Consumption Rate: %.2f kWh/nm | Dist Remaining %.1f nm' % (i, batt, cached_avg, range_remaining), end=' \r')
    #             # time.sleep(0.001)
    #         else:
    #             range_remaining = batt/roll_consumption   #nm
    #             # print('%d Batt: %.1f | Consumption Rate: %.2f kWh/nm | Dist Remaining: %.2f nm' % (i, batt, roll_consumption, range_remaining), end=' \r')
    #             # time.sleep(.001)

    #         dist_list.append(range_remaining)

    #     return dist_list