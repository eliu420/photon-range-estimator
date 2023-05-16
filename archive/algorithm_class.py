import math

class range_est():

    def __init__(self, battery_capacity, cached_avg, n_runs):
        self.max_battery = battery_capacity             # kWh
        self.cached_avg = cached_avg                    # kWh/nm
        self.n_runs = n_runs                            # int
        self.n_minutes = 5                              # interval for rolling average
        self.alpha = 0.15                               # Weighting Parameter
        self.range_remaining = 0                        # Range placeholder


    def overall_dist_avg(self, data):
        """This function evaluates range remaining on the battery given historical distance consumption data (kWh/nm) from all past trips."""
        self.range_remaining = data['energyAvailable']/self.cached_avg        # nautical miles


    def overall_time_avg(self, data, cached_avg):
        """This function evaluates range remaining on the battery given historical time consumption data (kWh/min) from all past trips."""
        time_remaining = data['energyAvailable']/cached_avg         # min 
        range_remaining = (time_remaining/60)*data['sog']           # nm

        return time_remaining, range_remaining
    

    def update_avg(self, data):
        """This function should be called whenever a trip is completed, updating the cached average.
        It stores the average consumption rate as well as the number of runs it is averaged over."""
        trip_avg = data['energyUsed']/data['tripDistance']                          # kWh/nm
        # new_avg = (nRuns*cached_avg + trip_avg)/(nRuns+1)
        # cached_avg = new_avg
        # nRuns += 1
        self.cached_avg = ((1-self.alpha)*self.cached_avg) + (self.alpha*trip_avg)
    

    def rolling_avg(self, data, nMins, roll_energy, roll_distance):
        """This function evaluates range remaining on the battery where 
        every nMins, roll_energy and roll_distance are updated accordingly to 
        calculate the rolling average consumption rate. A logarithmic scale is 
        applied to adjust value of the rolling average overtime. 
        """
        if data['tripDuration'] % nMins:
            curr_roll_energy = data['energyUsed'] - roll_energy
            curr_roll_distance = data['tripDistance'] - roll_distance
        
        roll_consumption = curr_roll_energy/curr_roll_distance
        curr_consumption = data['energyUsed']/data['tripDistance']
        
        """Might need to fix but idea is that weight to curr consumption
        only applies when log(10) < 1, otherwise it would be subtracting 
        a negative consumption rate which is incorrect (1-(n>=1)). 
        """
        weight = math.log(self.data['tripDuration'])
        if weight < 1:  
            roll_avg = weight * roll_consumption + (1-weight) * curr_consumption  
        roll_avg = weight * roll_consumption                                      

        range_remaining = int(data['energyAvailable']/roll_avg)
        return range_remaining, curr_roll_energy, curr_roll_distance
    