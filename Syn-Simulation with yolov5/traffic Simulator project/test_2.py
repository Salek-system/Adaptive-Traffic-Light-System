from trafficSimulator import *

# Create simulation
sim = Simulation()

# Add multiple roads
sim.create_roads([        
    ((0, 100) , (94, 100) , 100),    #0
    ((94, 100), (294, 100) , 110),   #1      300 -6 
    ((100, 98) , (100, 0) ,120),     #2    
    ((100, 104) , (100, 200),80),    #3       
])

sim.create_roads([  
    #==============================        
    ((300, 98)  , (300 ,0) ,100),    #4   down
    ((300 , 104) , (300,200),100),  #5   up     

])
sim.create_roads([  
    #=============================
    ((294, 100) , (444, 100) ,120),  #6   left to right traffic 3              
    ((450,98)   , (450 ,0) ,90),    #7 
    ((450, 104) , (450,200),65),   #8 

])
sim.create_roads([  
    #==============================
    ((444 ,100) , (600,100),110),   #9
])
    
sim.create_roads([ 
    #===========Reverse Road==========
    #=================================    
    ((600,106)  ,(456 ,106) ,110 ),  #10 -1     
    #=================================
    ((456, 106) ,(306, 106) ,110  ),  #11 -2          
    #=================================    
    ((306, 106) ,(106, 106) ,110),   #12 -3
    #=================================    
    ((106,106)  ,(0,106) ,110),      #13 -4

    # #=================================  
    # ((454,104)  ,(454 ,0) ),   #16
    # ((454,200) , (454 , 104) ),  #17 
    # #=================================
    # ((154, 104) , (154, 0)),   #6
    # ((154, 200) , (154, 104) ),  #7
    # #==================================
    # ( (304,200) , (304 , 104)),  # -4
    # ((304, 104) , (304 ,0) ),            
])


sim.create_gen({
    'vehicle_rate': 10, 
    'vehicles': [
        [1, {"path": [0, 1, 6, 9]}],    
        [1, {"path": [0, 2]}],    
        [1, {"path": [0, 1,4]}],    
        [1, {"path": [0, 1,6,7]}],    
                  
        [2, {"path": [10,11, 12,13]}],      
        [2, {"path": [10,8]}],      
        [2, {"path": [10,11,5]}],      
        [2, {"path": [10,11,12 ,3]}],      
    ]
})

# #sim.create_signal([[0],[1],[6]] )

sim.create_signal([[0]] )
sim.create_signal([[1]] )
sim.create_signal([[6]] )

# #sim.create_signal([[10],[11],[12]] ,index=1)
sim.create_signal([[10]] )
sim.create_signal([[11]] )
sim.create_signal([[12]] )

# Start simulation
win = Window(sim)
win.offset = (-300, -110)

#win.run(steps_per_update=15)
win.run(steps_per_update=1000)
