#RoadWatch
Computer vision project

This is an object detection model that detects incoming traffic on a highway in a video. 
It further counts the number of vehicles and displays their speeds on the video in real-time.

This project uses YOLOv8 model through ultralytics, and uses pretrained weights. 

SORT(Simple Online and Realtime Tracking) Algorithm used - https://github.com/abewley/sort

# Errors
If there is a problem in the installation of the lap library, please ensure you have g++ installed on your local machine and then try the installation again.
The speed calculation is not entirely accurate and must be configured to the video provided.
