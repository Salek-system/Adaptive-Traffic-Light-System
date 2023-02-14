# Adaptive-Traffic-Light-System

# Yolov5-detect-emergency

This module aims to help emergency vehicles by giving them the right of passage and crossing roads without waiting. First, we collected the dataset by photographing 1000 photos. We use toy emergency(ambulance, engine fire, police car) and non-emergency vehicles. Hence, we use the roboflow tool for labeling the images into two classifications emergency and non-emergency vehicles. Therefore, divide the labeled pictures into three categories that are train, test, and validate. Also,  for the implementation process of detecting emergency vehicles at intersections, we used the YOLOv5 algorithm. Moreover, the module sends pictures of the dataset to the synchronization module; if there are any emergency vehicles at the traffic light, it will control the traffic light and open it for the EV. That will improves emergency response times because the emergency vehicle will not have to slow down until the traffic lights control it.


# Contributers: 
