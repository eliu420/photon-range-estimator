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


    def parse_csv(self, df):
        self.data['sog'] = df['Speed m/s']*1.944
        self.data['time'] = df['Time']
        self.data['tripDistance'] = df['Distance km']*0.539957
        self.data['soc'] = df['SOC 1 %']
        self.data['packVoltage'] = df['Pack Voltage 1 V']*10
        self.data['packCurrent'] = df['Pack Current 1 A']
        self.data['power'] = self.data['packVoltage'] * self.data['packCurrent'] / 1000.0 # kW
        

        return self.data