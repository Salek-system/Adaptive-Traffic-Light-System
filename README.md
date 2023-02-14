# Salek: efficient and Adaptive Traffic Light System to Find Optimal Traffic Signal Synchronization and Giving the Right of Passage to Priority Vehicles.

# Syncronization module:
In this module, we model a network of roads to make a traffic simulation implemented in Python using pygame to be able to represent a simulation of synchronized traffic lights for straight intersections. We represented the roads with the graph algorithm. such as a directed graph G=(V, E), where: 
V is the set of vertices (or nodes).
And E is the set of edges that represent roads.
Every road is going to be explicitly defined by the values of its start and end nodes, which represent the distance with a specific speed for each road. In the simulation we won’t keep a set of nodes, instead, every road is going to be randomly defined by the values. We drew in the simulation 17 edges, which means 6 nodes. Moreover, we add vehicles stochastically according to pre-defined probabilities(Vehicle generation rate), which describe how many vehicles should be added to the simulation, on average, per minute. Every vehicle is going to have a path consisting of multiple roads (edges). We will apply the intelligent driver model for vehicles on the same road (the same edge we define). When a vehicle reaches the end of the first road,  we append it to the next road.

The traffic lights are placed at the vertices of roads and are characterized by two zones:
- Slow-down zone: characterized by a slow-down distance and a slow-down factor, is a zone in which vehicles slow down their maximum speed using the slow-down factor.
- Stop zone: characterized by a stop distance, is a zone in which vehicles stop. This is achieved using a damping force.


We will use the time equation to determine when the traffic light is opened based on the distance and speed of each intersection, to become the traffic lights are synchronized, and vehicles pass at a lower rate of time than the traditional traffic. 

# Detect Emergency Vehicle module:
This module aims to help emergency vehicles by giving them the right of passage and crossing roads without waiting. First, we collected the dataset by photographing 1000 photos. We use toy emergency(ambulance, engine fire, police car) and non-emergency vehicles. Hence, we use the roboflow tool for labeling the images into two classifications emergency and non-emergency vehicles. Therefore, divide the labeled pictures into three categories that are train, test, and validate. Also,  for the implementation process of detecting emergency vehicles at intersections, we used the YOLOv5 algorithm. Moreover, the module sends pictures of the dataset to the synchronization module; if there are any emergency vehicles at the traffic light, it will control the traffic light and open it for the EV. That will improves emergency response times because the emergency vehicle will not have to slow down until the traffic lights control it.

# Contributors:
Raneem Faisal Alrumaihi 

Reyam Mansour Alturki 

Farah Abdulaziz Alharbi 

Noura Abdullah Alwhaibi 

Mona Mohammed Alharbi 

Njoud Mohammed Almutairi 

Supervisor:

Dr. Ziyad Alsaeed
