# Yolov5-detect-emergency

This module aims to help emergency vehicles by giving them the right of passage and crossing roads without waiting. First, we collected the dataset by photographing 1000 photos. We use toy emergency(ambulance, engine fire, police car) and non-emergency vehicles. Hence, we use the roboflow tool for labeling the images into two classifications emergency and non-emergency vehicles. Therefore, divide the labeled pictures into three categories that are train, test, and validate. Also,  for the implementation process of detecting emergency vehicles at intersections, we used the YOLOv5 algorithm. Moreover, the module sends pictures of the dataset to the synchronization module; if there are any emergency vehicles at the traffic light, it will control the traffic light and open it for the EV. That will improves emergency response times because the emergency vehicle will not have to slow down until the traffic lights control it.

# Requirments:
To run this project, you need to do is:

First, download the labeled dataset.

Second, use google colab for training the dataset.

Third, use Jupyter notebook for testing the code locally.

# File structure: 
- [dataset](dataset) In this file, we display the dataset used in the project, divided into images of emergency vehicles and non-emergency vehicles.
- [README.dataset.txt](README.dataset.txt) Here is our training dataset in Roboflow with labeled photos.
- [data.yaml](data.yaml) This file provides details of the training path and classification.  
- [dataset-images-and-labels](dataset-images-and-labels) This file represents three internal files. The file is a test, train, and valid. Each file has two sub fils images files and labeled files.
- [yolov5_custom_training.py](yolov5_custom_training.py) Google colab file, and it has the training code.
- [yolov5_detect.ipynb](yolov5_detect.ipynb) This file code is for testing the detect model locally in Jupyter notebook.
