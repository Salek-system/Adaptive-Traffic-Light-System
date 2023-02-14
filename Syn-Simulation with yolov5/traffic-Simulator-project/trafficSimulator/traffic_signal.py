import random


class TrafficSignal:

    def __init__(self, roads, config={}, i=0, roads_ids=[]):

        # Initialize roads
        self.roads = roads
        self.roads_ids = roads_ids

        # Set default configuration
        self.set_default_config(i)

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()

    def __repr__(self):
        return f"TrafficSignal({self.roads}, {self.current_cycle_index})"

    def set_default_config(self, i=0):
        self.cycle = [(False, True), (True, False)]
        
        self.slow_distance = 50        
        self.slow_factor = 0.4        
        self.stop_distance = 20       
        self.current_cycle_index = i
        self.last_t = 0
        
        """ self.slow_distance = 50        
        self.slow_factor = 0.4        
        self.stop_distance = 15        
        self.current_cycle_index = i
        self.last_t = 0 """

        # self.state = False
        # self.state = bool(random.choice([True, False]))
        self.state = bool(random.getrandbits(1))
        self.LightGreen = 0        
        self.timerGreen = 0
        self.LightRed = 30
        self.timerRed = 30 

    def init_properties(self):
        for i in range(len(self.roads)):
            for road in self.roads[i]:
                # Add Property time traffic signal
                self.timerGreen = road.traffic_signal_time
                self.LightGreen = road.traffic_signal_time
                
                road.set_traffic_signal(self, i)               

    @property
    def current_cycle(self):        
        return self.cycle[self.current_cycle_index]
    
    @property
    def current_state(self):
        # add property state for traffic signal light (green - read)
        return self.state

    def stop(self):
        self.state = False  # Red

    def unstop(self):
        self.state = True  # Green
   
    def update(self, sim):
        # cycle_length = 30
        cycle_length = self.timerGreen    
        k = (sim.t // cycle_length) % 2                                
        self.current_cycle_index = int(k)      

        if self.timerRed == 0:
            self.unstop()
        else:
            self.stop()
