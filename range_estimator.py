
import math

class range_est():

    def __init__(self, battery_capacity, dist_avg, time_avg, n_runs, roll_energy, roll_distance):
        self.max_battery = battery_capacity                         # kWh
        self.dist_avg = dist_avg                                    # kWh/nm
        self.time_avg = time_avg                                    # kWh/min
        self.n_runs = n_runs                                        # int
        self.range_remaining = 0                                    # nm        
        self.time_remaining = 0                                     # min
        self.alpha = 0.15                                           # Weighting parameter
        
        # used for rolling avg
        self.n_mins = 10                                             # interval for updating rolling average
        self.roll_energy = roll_energy                              # last energy useage, updated every n_mins
        self.roll_distance = roll_distance                          # last distance traveled, updated every n_mins
        self.roll_avg = 0 
        self.roll_consumption = 0


    def tick(self, data):
        self.overall_dist_avg(data) 


    def overall_dist_avg(self, data):
        """This function evaluates range remaining on the battery given historical distance consumption data (kWh/nm) from all past trips."""
        self.range_remaining = data['energyAvailable']/self.dist_avg        # nautical miles


    def overall_time_avg(self, data):
        """This function evaluates range remaining on the battery given historical time consumption data (kWh/min) from all past trips."""
        self.time_remaining = data['energyAvailable']/self.time_avg         # min 
        trip_speed = data['tripDistance']/data['tripDuration']*3600
        self.range_remaining = (self.time_remaining/60)*trip_speed        # nm


    def rolling_avg(self, data):
        # Ryan's version
        """This function evaluates range remaining on the battery where 
        every nMins, roll_energy and roll_distance are updated accordingly to 
        calculate the rolling average consumption rate. A fractional scale is 
        applied to adjust weight of the rolling average overtime."""

        if (data['tripDuration']/60) % self.n_mins == 0:
            curr_roll_energy = data['energyUsed'] - self.roll_energy
            curr_roll_distance = data['tripDistance'] - self.roll_distance
            self.roll_consumption = curr_roll_energy/curr_roll_distance
            self.roll_energy = data['energyUsed']
            self.roll_distance = data['tripDistance']

        weight = 'n/a'
        t = 'n/a'

        if (data['tripDuration']/60) <= self.n_mins:
            self.roll_avg = self.dist_avg
        elif (data['tripDuration']/60) > self.n_mins:
            t = (data['tripDuration']/60) - self.n_mins
            # weight = t/(t+self.n_mins)
            weight = 0.15
            self.roll_avg = ((1-weight)*self.dist_avg) + (weight*self.roll_consumption)

        self.range_remaining = data['energyAvailable']/self.roll_avg


    def update_avg(self, data):
        """This function should be called whenever a trip is completed, updating the cached average.
        It stores the average consumption rate as well as the number of runs it is averaged over."""

        dist_avg = data['energyUsed']/data['tripDistance']              # kWh/nm
        new_dist_avg = (self.n_runs*self.dist_avg + dist_avg)/(self.n_runs+1)
        self.dist_avg = new_dist_avg
        # self.dist_avg = ((1-self.alpha)*self.dist_avg) + (self.alpha*dist_avg)

        time_avg = data['energyUsed']/data['tripDuration']*60              # kWh/min
        new_time_avg = (self.n_runs*self.time_avg + time_avg)/(self.n_runs+1)
        self.time_avg = new_time_avg
        # self.time_avg = ((1-self.alpha)*self.time_avg) + (self.alpha*time_avg)
    
        self.n_runs += 1



    def rolling_avg1(self, data, nMins, roll_energy, roll_distance):
        # Elliot's version
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
                              

    


    

    
        