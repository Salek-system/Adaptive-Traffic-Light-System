from random import randint
import time
import logging
import threading
from typing import Dict
from collections import defaultdict

import pygame
from pygame import gfxdraw
import numpy as np

from trafficSimulator.config import *


from yolov5.detect import DetectEmergency
from yolov5.utils.general import check_requirements

RECORDS_FILE_NAME = f"simulation_data_{time.time()}.csv"

#import os
#os.chdir("yolov5") 

class Window:
    def __init__(self, sim, config={}):

        self.logger = logging.getLogger(self.__class__.__name__)

        # TODO: what are the records we are collecting, this is what I know so far
        #   - time_s: this is the self.sim.t we need to know for sure the unit of this variable.
        #   - frame: The frame count of the simulation.
        #   - system_level_vehicle_count: The total number of vehicles in the simulation now.
        #   - H1: The number of vehicles on the road H1 now.
        #   - H2: The number of vehicles on the road H2 now.
        #   - V1: The number of vehicles on the road V1 now.
        #   - V2: The number of vehicles on the road V2 now.
        #   - V3: The number of vehicles on the road V3 now.
        #   - traffic-light-status-H1-0:
        #   - traffic-light-count-H1-0:

        # write the header of the CSV file, We must know how many columns we have from this point
        self.csv_header_list = ['time_s', 'frame', 'system_level_vehicle_count']
        for road_info in RoadsNames:
            self.csv_header_list.append(str(road_info.name))

        for tf_idx in [0, 1, 2, 3, 5, 7, 8, 9, 12, 13, 15, 16]:
            road_id = None
            for road_info in RoadsNames:
                if tf_idx in road_info.value:
                    road_id = road_info.name
            self.csv_header_list.append(f"traffic-light-status-{road_id}-{tf_idx}")
            self.csv_header_list.append(f"traffic-light-count-{road_id}-{tf_idx}")

        with open(RECORDS_FILE_NAME, 'w') as records_file:
            records_file.write(",".join(self.csv_header_list))
        self.logger.info(
            f"len(self.csv_header_list)={len(self.csv_header_list)}, self.csv_header_list={self.csv_header_list}")
        # a dictionary to collect a data record for each round.
        self.records = defaultdict(int)

        self.value = 0  # vehicle is normal

        # Simulation to draw
        self.sim = sim

        # initially, all configuration are set to null
        self.width = None
        self.height = None
        self.bg_color = None
        self.fps = None
        self.zoom = None
        self.offset = None
        self.mouse_last = None
        self.mouse_down = None
        self.screen = None

        # Set default configurations
        self.set_default_config()

        # Update configurations
        for attr, val in config.items():
            setattr(self, attr, val)
        
    def set_default_config(self):
        """Set default configuration"""
        self.width = 1360
        self.height = 760
        self.bg_color = (250, 250, 250)

        # self.fps = 60
        self.fps = 6
        
        # self.zoom = 5
        self.zoom = 2.5
        self.offset = (0, 0)

        self.mouse_last = (0, 0)
        self.mouse_down = False

    def deamonThread (self):
        while True:
            #self.logger.debug("Sending Out Signal Detected Emergency Vehicle")
            
            detected = DetectEmergency (
            weights=  'best.pt' ,
            conf= 0.5  ,
            img_size=  (416,416),
            source=  'test2.jpg'
            )
            opt = detected.parse_opt()

            check_requirements(exclude=('tensorboard', 'thop'))

            detected.run( **vars(opt))

            print (detected.current_detected)
            if detected.current_detected:
                self.value = 99  # vehicle is emergency
            
            time.sleep(10)    # Every 10 second detect vehicle is emergency  
            
            

          

    def loop(self, loop=None):
        """Shows a window visualizing the simulation and runs the loop function."""
      
        # Create a pygame window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.flip()

        # Fixed fps
        clock = pygame.time.Clock()

        # To draw text
        pygame.font.init()
        self.text_font = pygame.font.SysFont('Lucida Console', 16)

        daemonThread = threading.Thread(name="DetetctedEmeregencyVehicle" , target=self.deamonThread)
        daemonThread.setDaemon(True)
        daemonThread.start()

        #i= 0
        # Draw loop
        running = True
        while running:
            # Update simulation
            # print ("External loop i = {} , value = {}".format(i , self.value))
            # i += 1
            if loop: loop(self.sim)

            # Draw simulation
            self.draw()
            # print (self.value)
            # Update window
            pygame.display.update()
            # print (self.fps)
            clock.tick(self.fps)

            # Handle all events
            for event in pygame.event.get():
                # Quit program if window is closed
                if event.type == pygame.QUIT:
                    running = False
                # Handle mouse events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If mouse button down
                    if event.button == 1:
                        # Left click
                        x, y = pygame.mouse.get_pos()
                        x0, y0 = self.offset
                        self.mouse_last = (x-x0*self.zoom, y-y0*self.zoom)
                        self.mouse_down = True
                    if event.button == 4:
                        # Mouse wheel up
                        self.zoom *=  (self.zoom**2+self.zoom/4+1) / (self.zoom**2+1)
                    if event.button == 5:
                        # Mouse wheel down 
                        self.zoom *= (self.zoom**2+1) / (self.zoom**2+self.zoom/4+1)
                elif event.type == pygame.MOUSEMOTION:
                    # Drag content
                    if self.mouse_down:
                        x1, y1 = self.mouse_last
                        x2, y2 = pygame.mouse.get_pos()
                        self.offset = ((x2-x1)/self.zoom, (y2-y1)/self.zoom)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_down = False           

    def run(self, steps_per_update=1):
        """Runs the simulation by updating in every loop."""
        def loop(sim):
            sim.run(steps_per_update)
            
        self.loop(loop)

    def convert(self, x, y=None):
        """Converts simulation coordinates to screen coordinates"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (
            int(self.width/2 + (x + self.offset[0])*self.zoom),
            int(self.height/2 + (y + self.offset[1])*self.zoom)
        )

    def inverse_convert(self, x, y=None):
        """Converts screen coordinates to simulation coordinates"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (
            int(-self.offset[0] + (x - self.width/2)/self.zoom),
            int(-self.offset[1] + (y - self.height/2)/self.zoom)
        )

    def background(self, r, g, b):
        """Fills screen with one color."""
        self.screen.fill((r, g, b))

    def line(self, start_pos, end_pos, color):
        """Draws a line."""
        gfxdraw.line(
            self.screen,
            *start_pos,
            *end_pos,
            color
        )

    def rect(self, pos, size, color):
        """Draws a rectangle."""
        gfxdraw.rectangle(self.screen, (*pos, *size), color)

    def box(self, pos, size, color):
        """Draws a rectangle."""
        gfxdraw.box(self.screen, (*pos, *size), color)

    def circle(self, pos, radius, color, filled=True):
        gfxdraw.aacircle(self.screen, *pos, radius, color)
        if filled:
            gfxdraw.filled_circle(self.screen, *pos, radius, color)

    def polygon(self, vertices, color, filled=True):
        gfxdraw.aapolygon(self.screen, vertices, color)
        if filled:
            gfxdraw.filled_polygon(self.screen, vertices, color)

    def rotated_box(self, pos, size, angle=None, cos=None, sin=None, centered=True,
    color=(0 , 0, 255), filled=True):
        """Draws a rectangle center at *pos* with size *size* rotated anti-clockwise by *angle*."""
        # red (255, 0, 0)  ,  yellow(255 ,255 ,0) , blue (0, 0, 255)
        x, y = pos
        l, h = size

        if angle:
            cos, sin = np.cos(angle), np.sin(angle)

        vertex = lambda e1, e2: (
            x + (e1*l*cos + e2*h*sin)/2,
            y + (e1*l*sin - e2*h*cos)/2
        )

        if centered:
            vertices = self.convert(
                [vertex(*e) for e in [(-1,-1), (-1, 1), (1,1), (1,-1)]]
            )
        else:
            vertices = self.convert(
                [vertex(*e) for e in [(0,-1), (0, 1), (2,1), (2,-1)]]
            )

        self.polygon(vertices, color, filled=filled)

    def rotated_rect(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=(0, 0, 255)):
        self.rotated_box(pos, size, angle=angle, cos=cos, sin=sin, centered=centered, color=color, filled=False)

    def arrow(self, pos, size, angle=None, cos=None, sin=None, color=(150, 150, 190)):
        if angle:
            cos, sin = np.cos(angle), np.sin(angle)
        
        self.rotated_box(
            pos,
            size,
            cos=(cos - sin) / np.sqrt(2),
            sin=(cos + sin) / np.sqrt(2),
            color=color,
            centered=False
        )

        self.rotated_box(
            pos,
            size,
            cos=(cos + sin) / np.sqrt(2),
            sin=(sin - cos) / np.sqrt(2),
            color=color,
            centered=False
        )
   
    #draw axes
    def draw_axes(self, color=(100, 100, 100)):
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.width, self.height)
        self.line(
            self.convert((0, y_start)),
            self.convert((0, y_end)),
            color
        )
        self.line(
            self.convert((x_start, 0)),
            self.convert((x_end, 0)),
            color
        )

    def draw_grid(self, unit=50, color=(150,150,150)):
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.width, self.height)

        n_x = int(x_start / unit)
        n_y = int(y_start / unit)
        m_x = int(x_end / unit)+1
        m_y = int(y_end / unit)+1

        for i in range(n_x, m_x):
            self.line(
                self.convert((unit*i, y_start)),
                self.convert((unit*i, y_end)),
                color
            )
        for i in range(n_y, m_y):
            self.line(
                self.convert((x_start, unit*i)),
                self.convert((x_end, unit*i)),
                color
            )

    def draw_roads(self):
        for road in self.sim.roads:
            # Draw road background
            self.rotated_box(
                road.start,
                (road.length, 3.7),
                cos=road.angle_cos,
                sin=road.angle_sin,
                color=(180, 180, 220),
                centered=False
            )
            # Draw road lines
            # self.rotated_box(
            #     road.start,
            #     (road.length, 0.25),
            #     cos=road.angle_cos,
            #     sin=road.angle_sin,
            #     color=(255, 255, 255),
            #     centered=False
            # )

            # Draw road arrow
            if road.length > 15: 
                for i in np.arange(-0.5*road.length, 0.5*road.length, 10):
                    pos = (
                        road.start[0] + (road.length/2 + i + 3) * road.angle_cos,
                        road.start[1] + (road.length/2 + i + 3) * road.angle_sin
                    )

                    self.arrow(
                        pos,
                        (-1.25, 0.2),
                        cos=road.angle_cos,
                        sin=road.angle_sin
                    )              
            # TODO: Draw road arrow

    def draw_vehicle(self, vehicle, road):
        """
        A method to draw a single vehicle within a road segment.

        :param vehicle:
        :param road:
        """
        l, h = vehicle.l, 2
        sin, cos = road.angle_sin, road.angle_cos       

        x = road.start[0] + cos * vehicle.x 
        y = road.start[1] + sin * vehicle.x         
        
        # red (255, 0, 0) , yellow(255 ,255 ,0) , blue (0, 0, 255) defulat
        if vehicle.isEmergency :
            self.rotated_box((x, y), (l, h), cos=cos, sin=sin,  centered=True , color=(255 ,255 ,0))        
        else:
            self.rotated_box((x, y), (l, h), cos=cos, sin=sin,  centered=True )
      
    def draw_vehicles(self):
        """
        A method to draw more than one vehicle.
        """
        i = 0 

        self.records["system_level_vehicle_count"] = 0

        for segment_id, road in enumerate(self.sim.roads, start=0):
            #self.logger.debug(f"segment_id={segment_id}, road={road}, road.vehicles={road.vehicles}")

            # for data collection use only
            road_id = None
            for road_name in RoadsNames:
                if segment_id in road_name.value:
                    road_id = road_name.name
            assert road_id is not None

            # add the number of vehicle in a segment to its road id.
            self.records[road_id] += len(road.vehicles)

            # count  vehicle in system
            self.records["system_level_vehicle_count"] += len(road.vehicles)

            #self.logger.debug(f"self.records={self.records}")

            for vehicle in road.vehicles:
                # i = 0 mean vehicle go from left to right                                     
                if (self.value == 99 and i in [0,2,7,13,16]  and not vehicle.isEmergency) :  # i=10 mean go from right to left
                    vehicle.isEmergency = True
                    self.value = 0    
                else:
                    self.value = 0                    
                self.draw_vehicle(vehicle, road )

         

            i += 1

    
    def draw_signals(self):
        #self.logger.debug("Refresh the signals? ...")

        global b  # TODO: I don't see why this is a global! It can be a simple boolean.
        for signal in self.sim.traffic_signals:  # looping through all signals
            #self.logger.debug(f"Current signal={signal}")

            for i in range(len(signal.roads)):                                    
                color = (0, 255, 0) if signal.current_cycle[i] else (255, 0, 0)   # current cycle
                b = False 
                for road in signal.roads[i]:                                            
                  
                    for vehicle in road.vehicles:
                        if vehicle.isEmergency :
                            b = True
                            print ("vehicle in road is vehicle = {} ".format(b))
                            break
                    if b :                        
                        color = (0, 255, 0)   #Traffic Color Equal Green

                    a = 0
                    position = (
                        (1-a)*road.end[0] + a*road.start[0],
                        (1-a)*road.end[1] + a*road.start[1]
                    )
                    self.rotated_box(
                        position,
                        (1, 3),
                        cos=road.angle_cos, sin=road.angle_sin,
                        color=color)
                  
                  
                    # self.logger.debug(f"selected road={road}, position={position}")
                    # self.logger.debug(f"index={i}, road_id_in_signal={signal.roads_ids[i]}")
                    # self.logger.debug(f"signal.idx={signal.current_cycle_index}")

                    # collecting signal data for analysis
                    road_id = None
                    for road_info in RoadsNames:
                        if signal.roads_ids[i] in road_info.value:
                            road_id = road_info.name
                    traffic_signal_name = f"{road_id}-{signal.roads_ids[i]}"


                    self.records[f"traffic-light-status-{traffic_signal_name}"] = "G" if signal.current_cycle[i] else "R"
                    self.records[f"traffic-light-count-{traffic_signal_name}"] = 0 if signal.current_cycle[i] else len(road.vehicles)
                    #self.logger.debug(f"Signal={signal.current_cycle[i]}, has current state={signal.current_cycle[i]}")




    def draw_status(self):
        # self.logger.debug("Updating status ...")
        # self.logger.debug(f"self.sim.t={self.sim.t}, self.sim.frame_count={self.sim.frame_count}")
        self.records['time_s'] = round(self.sim.t, 2)
        self.records['frame'] = int(self.sim.frame_count)

        text_fps = self.text_font.render(f't={self.sim.t:.5}', False, (0, 0, 0))
        text_frc = self.text_font.render(f'n={self.sim.frame_count}', False, (0, 0, 0))
        
        self.screen.blit(text_fps, (0, 0))
        self.screen.blit(text_frc, (100, 0))

        self.write_record_to_existing_csv_file()

    def draw(self ):
        # Fill background
        self.background(*self.bg_color)

        # Major and minor grid and axes
        # self.draw_grid(10, (220,220,220))
        # self.draw_grid(100, (200,200,200))
        # self.draw_axes()

        self.draw_roads()
        self.draw_vehicles()
        self.draw_signals()

        # Draw status info
        self.draw_status()

    def write_record_to_existing_csv_file(self):

        # TODO: Can we collect all the data here and not in each function?
        #   This will guarantee that the data is consistent! Either way is fine for the project!
        #self.logger.info(f"len(self.records)={len(self.records)}, self.records={self.records}")
        record = []
        for header in self.csv_header_list:
            record.append(str(self.records.get(header, "empty")))

        with open(RECORDS_FILE_NAME, 'a') as records_file:
            records_file.write("\n"+",".join(record))
        #self.logger.info(f"len(self.csv_header_list)={len(self.csv_header_list)}, self.csv_header_list={self.csv_header_list}")
        #self.logger.info(f"len(record)={len(record)}, record={record}")

        self.records = defaultdict(int)
