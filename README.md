# Yolov5-detect-emergency



#Requirments:
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
