# Object Detection Analyzer

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
