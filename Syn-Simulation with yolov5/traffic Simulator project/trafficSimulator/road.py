from scipy.spatial import distance
from collections import deque


class Road:
    def __init__(self, start, end, speed):
        self.start = start
        self.end = end
        self.speed = speed
        self.vehicles = deque()
        self.init_properties()

    def __repr__(self):
        return f"Road({self.start}, {self.end})"

    def init_properties(self):
       
        self.length = distance.euclidean(self.start, self.end)
        self.angle_sin = (self.end[1]-self.start[1]) / self.length
        self.angle_cos = (self.end[0]-self.start[0]) / self.length
        # self.angle = np.arctan2(self.end[1]-self.start[1], self.end[0]-self.start[0])
        self.has_traffic_signal = False
        self.time = 0  # time for  traffic sign  (Light Green)

    def set_traffic_signal(self, signal, group):
        self.traffic_signal = signal
        self.traffic_signal_group = group
        self.has_traffic_signal = True

    @property
    def traffic_signal_state(self):
        if self.has_traffic_signal:
            i = self.traffic_signal_group            
            return self.traffic_signal.current_cycle[i]            
        return True

    @property
    def traffic_signal_state_time(self):
        if self.has_traffic_signal:            
            return self.traffic_signal.current_state
        return True

    @property
    def traffic_signal_time(self):
        # self.time = (self.length / self.speed) *10
        self.time = int((self.length / self.speed)*10)
        # print (self.time)
        return self.time
        
    def update(self, dt):
        n = len(self.vehicles)

        if n > 0:
            # Update first vehicle
            self.vehicles[0].update(None, dt)
            # Update other vehicles
            for i in range(1, n):
                lead = self.vehicles[i-1]
                self.vehicles[i].update(lead, dt)

            # Check for traffic signal
            # if self.traffic_signal_state_time:
            if self.traffic_signal_state:
                # If traffic signal is green or doesn't exist
                # Then let vehicles pass
                self.vehicles[0].unstop()
                for vehicle in self.vehicles:
                    vehicle.not_slow()
            else:
                # If traffic signal is red            
                if self.vehicles[0].x >= self.length - self.traffic_signal.slow_distance:
                    # Slow vehicles in slowing zone
                    self.vehicles[0].slow(self.traffic_signal.slow_factor*self.vehicles[0]._v_max)

                if self.vehicles[0].x >= self.length - self.traffic_signal.stop_distance and \
                        self.vehicles[0].x <= self.length - (self.traffic_signal.stop_distance / 2):
                    # Stop vehicles in the stop zone
                    self.vehicles[0].stop()
