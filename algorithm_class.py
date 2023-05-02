
class range_est():

    def __init__(self, battery_capacity):
        self.max_battery = battery_capacity                         # kWh    


    def overall_dist_avg(self, data, cached_avg):
        """This function evaluates range remaining on the battery given historical distance consumption data (kWh/nm) from all past trips."""
        range_remaining = int(data['energyAvailable']/cached_avg)        # nautical miles

        return range_remaining


    def overall_time_avg(self, data, cached_avg):
        """This function evaluates range remaining on the battery given historical time consumption data (kWh/min) from all past trips."""
        time_remaining = data['energyAvailable']/cached_avg         # min 
        range_remaining = (time_remaining/60)*data['sog']           # nm

        return time_remaining, range_remaining


    def rolling_avg(self, cached_avg, N_minutes):
        """This function updates the range based on the trip duration. 
        Range will be calculated based on cached_avg (cached average energy consumption) for the first N minutes of the trip.
        After N minutes, range will be calculated with the average consumption for the given trip."""

        # Need a way to update rolling average every N minutes
        roll_consumption = self.data['energyUsed']/self.data['tripDistance']        # kWh/nm

        if self.data['tripDuration'] < N_minutes or roll_consumption==0:
            range_remaining = self.data['energyAvailable']/cached_avg
        else:
            # Insert a weighting function here (logarithmic?)
            range_remaining = self.data['energyAvailable']/roll_consumption         # nm

        return range_remaining, roll_consumption
    

    def update_avg(self, data, cached_avg, nRuns):
        """This function should be called whenever a trip is completed, updating the cached average.
        It stores the average consumption rate as well as the number of runs it is averaged over."""
        trip_avg = data['energyUsed']/data['tripDistance']                          # kWh/nm
        new_avg = (nRuns*cached_avg + trip_avg)/(nRuns+1)
        cached_avg = new_avg
        nRuns += 1

        return cached_avg, nRuns
    

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