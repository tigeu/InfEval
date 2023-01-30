# InfEval: Application for Object Detection Analysis

This project provides a tool that can be used to further analyze your object detection models. You can upload your 
dataset and a model to start an inference task running on the backend, reporting the progress back to you. The result
can be further analyzed in the main view using several filtering options. If you uploaded a label map and ground truth
file as well, you can also calculate the COCO detection metric and pascal voc metric basen on your selected settings.

## Installation

1. Clone this repository using HTTPS<br>
   ```https://github.com/tigeu/ObjectDetectionAnalyzer.git```
   <br>or SSH<br>
   ```git@github.com:tigeu/ObjectDetectionAnalyzer.git```

2. Install [Python 3.9](https://www.python.org/downloads/release/python-390/)

3. Install [NodeJS](https://nodejs.org/en/download/)

4. Navigate to the ObjectDetectionAnalyzer 

5. Clone submodules<br>
   ```git submodule init && git submodule update```

6. Install backend   
   - Navigate to ObjectDetectionAnalyzer/Backend
   - Install necessary libraries<br>
   ```pip install -r requirements.txt```
   - Navigate to ObjectDetectionAnalyzer/Backend/metric/review_object_detection_metrics and install the repository<br>
   ```pip install . ```
   - Navigate back to ObjectDetectionAnalyzer/Backend/
   - Initialise SQLite database<br>
   ```python manage.py migrate```

7. Install Frontend
   - Navigate to ObjectDetectionAnalyzer/Frontend
   - Install necessary libraries<br>
   ```npm install```

8. Run backend server
   ```python manage.py runserver```

9. Run frontend server
   ```ng serve --open```

## System Architecture
The system architecture used here is a server-client architecture represented by back end and front end. The communication between those two main components uses entirely HTTP requests. For user authentication and authorization PyJWT is used. Alongside TensorFlow1/2 and PyTorch, the application also allows YOLOv3 and YOLOv5 models (implementations by ultralytics). For calculating the COCO and PascalVOC metrics we use the implementation of rafaelpadilla (https://github.com/rafaelpadilla/review\_object\_detection\_metrics.git).

### Backend
The back end is implemented in Python 3.9 using the Django REST framework. As the most machine learning frameworks are written in Python, this choice allows us to easily include those into our project.
The implementation supports multiple different users, each with its personal folder structure for uploads. In order to keep track of all uploaded files for every user there is an SQLite3 database to store user information alongside meta data i.e. path to the data set or the availability of its according ground truth values for faster processing of requests of the administered data. Using this meta data, the file system does not have to be accessed for every HTTP request.

### Frontend
The front end is implemented in TypeScript using the Angular framework. It allows a modular build-up providing an own component for each contributed functionality. Individual components have a corresponding unit to contact with using the RESTful API. A modular design allows a straightforward extension and an easy maintainability. 
The GUI is designed with Bootstrap 5 and Angular Material UI. Those frameworks make it very easy to create a powerful, responsive web design with the ability to adapt to different screen sizes and scale its components. They also support cross-browser compatibility which is a great advantage in case different browsers are in use.

## Components
### Register
Click on the link below the login view in ordert o access the registration. An account is required in order to store 
and access your personal data. The username has to be alphanumeric, the email has to be valid and the password has no
requirements. After successfully registering you are redirected to Login component.

### Login
Login with your supplied credentials from registration. After successfully registration you are redirected to Main 
component.

### Main
This component contains all utitilies to further investigate your dataset and your predictions. On the top left, you 
can select a dataset from your uploaded Datasets. After selecting a dataset, you can see all its image files listed 
below. Those image files can be filtered in the field above. If you select an image, it will be displayed in the center
of your screen, fully using the available space. On the right of the screen you can see the toolbox. Depending on the
data you supplied for your dataset, different tools are available. <br>
#### Ground Truth utilities
If you uploaded a valid ground truth file, its values can be shown on the selected image by ticking the checkbox. In
the ground truth settings section you can further customize different drawing settings and also remove classes or labels.
#### Prediction settings
If you uploaded a valid prediction file or ran an inference task on this dataset, the predictions can be shown on the 
selected image by ticking the checkbox. Just like the ground truth abilities, you can customize these drawings as well. <br>
Additionally, predictions can be further filtered by a confidence interval and non-max suppression. <br>
If you also uploaded ground truth values, you can visualize the matched ground truth values by entering an IoU threshold
that should be reached in order to count as a match. Ticking "Match transparent" will remove the background filling,
ticking "Only show matches" removes all drawings for predictions. <br>
You can also calculate the Pascal VOC metric and coco detection metric using the current settings (unchecked classes are
not considered; filtering settings are used). After selecting a metric you can click the button to calculate it for image
or for the dataset. The results will be displayed below, for the entire image (or whole dataset) and for each class. 
The library used for metric calculation can be found [here](https://github.com/rafaelpadilla/review_object_detection_metrics/).

### Upload
Use this component to upload your data. If the upload is successfull, a success message will be displayed. In case of
an invalid file, an error message will appear.
#### Dataset
A dataset has to be supplied as a zip file from which all images (.png, .jpg) will be extracted and saved.
#### Ground Truth
To upload ground truth values, you have to select a target dataset and each ground truth values has to be in the 
following format: <br>
```image_name class_name xmin ymin xmax ymax```
#### Prediction
To upload prediction values, you have to select a target dataset and each prediction has to be in the following format: <br>
```image_name class_name confidence xmin ymin xmax ymax```

#### Model
To upload a model, you have to select one of the supported types: 
[TensorFlow 1 or 2](https://www.tensorflow.org/), [PyTorch](https://pytorch.org/), 
[YOLOv3](https://github.com/ultralytics/yolov3) or [YOLOv5](https://github.com/ultralytics/yolov5). <br>
Also a model name is required to be used in an inference task.

#### Label map
To upload a label amp, you have to select a target model and the file has to be in JSON format: <br>
```{ "1": "class1", "2": "class2" }``` <br>
If you don't supply a label map, the metric will not be calculated and the class number will be shown in the drawings.

### Tasks
If you uploaded a valid model, you can start an inference task. Every task requires a unique name, a file name (for 
results), a dataset and a model. A description is optional. After you started a task, its progress will be shown on
the right side with a progress bar. To stop a task, you can use Overview and delete it.

### Overview
This overview shows all your uploads for this user and also provides the ability to delete certain uploads using the 
icon on the right. Keep in mind that all related data will be deleted as well, so if you delete a dataset all tasks will
be stopped, all predictions deleted etc.

## Screenshots
### Start inference task
![InferenceTask](https://user-images.githubusercontent.com/49535253/197328935-552caf22-949e-4e6a-b6f6-6ca55f541b70.png)

### View Ground Truth
![ViewGroundTruth](https://user-images.githubusercontent.com/49535253/197328956-bbebcc9f-3002-45d2-b604-59b722896003.png)

### Filter Predictions 
![FilterPredictions](https://user-images.githubusercontent.com/49535253/197328993-80b32a45-43da-48ce-b859-6f96f7b935a1.png)

### Calculate Metric
![CalculateMetric](https://user-images.githubusercontent.com/49535253/197328982-d8e714cd-00f6-4921-a5e3-13104253688d.png)


## Demos
### Design Ground Truth
https://user-images.githubusercontent.com/49535253/197328630-ec8a24b9-ffc2-4e6e-a848-8da5b4747189.mp4

### Upload Model
https://user-images.githubusercontent.com/49535253/197328735-1e5c453b-17c7-49b4-8cef-da5eb660ca46.mp4

### Start inference task
https://user-images.githubusercontent.com/49535253/197328659-6aab6450-cbca-44cc-a2de-85107b75bca0.mp4

### Analyze predictions
https://user-images.githubusercontent.com/49535253/197328557-45778ffe-2f62-4f3d-b28c-ce18f5d0f48d.mp4
