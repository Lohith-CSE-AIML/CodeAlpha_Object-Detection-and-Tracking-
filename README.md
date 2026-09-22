# Object Detection & Tracking

A real-time object detection and tracking web application built using **YOLO11, ByteTrack, OpenCV, Flask, HTML, CSS, and JavaScript**.

The application allows users to upload a video and processes it frame by frame to detect and track objects. It displays bounding boxes, object labels, confidence scores, tracking IDs, object counts, and IN/OUT counts through a web dashboard.

---

## 🚀 Features

* Upload a video through a web interface
* Real-time object detection using YOLO11
* Object tracking using ByteTrack
* Bounding boxes around detected objects
* Object class labels
* Confidence scores
* Unique tracking IDs
* Center points for tracked objects
* Virtual counting line
* IN/OUT object counting
* Current object count
* Detection class statistics
* Live processed video feed
* Automatic statistics updates
* Responsive web interface
* Flask backend
* HTML, CSS, and JavaScript frontend

---

## 🛠️ Technologies Used

### Machine Learning / Computer Vision

* YOLO11
* ByteTrack
* OpenCV
* Ultralytics

### Backend

* Python
* Flask
* Gunicorn

### Frontend

* HTML
* CSS
* JavaScript

### Deployment & Version Control

* Render
* GitHub

---

## 📁 Project Structure

```text
Object_Detection/
│
├── app1.py
├── object_tracking.py
├── yolo11n.pt
├── requirements.txt
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── script.js
│
└── uploads/
    └── .gitkeep
```

---

## 🧠 How It Works

The application follows this pipeline:

```text
User Uploads Video
        ↓
      Flask
        ↓
 Read Video Frame
        ↓
      YOLO11
        ↓
 Object Detection
        ↓
    ByteTrack
        ↓
 Object Tracking
        ↓
 Bounding Boxes + IDs
        ↓
   IN / OUT Counting
        ↓
 Processed Frame
        ↓
 Flask Video Stream
        ↓
 Web Dashboard
```

### Step 1: Video Upload

The user selects a video through the web interface and clicks **Start Detection**.

The frontend sends the video to the Flask backend using the `/upload` endpoint.

### Step 2: Flask Backend

Flask receives the uploaded video and stores it temporarily in the `uploads/` directory.

The backend then starts processing the video frame by frame.

### Step 3: Read Video Frames

OpenCV is used to open the uploaded video and read individual frames.

Each frame is passed to the YOLO11 model for object detection.

### Step 4: Object Detection with YOLO11

YOLO11 analyzes every frame and identifies objects such as:

```text
person
car
bus
truck
bicycle
backpack
```

For every detected object, YOLO11 provides:

* Object class
* Bounding box
* Confidence score

### Step 5: Object Tracking with ByteTrack

The detected objects are passed to ByteTrack.

ByteTrack assigns a unique tracking ID to objects and attempts to maintain the same ID across consecutive frames.

For example:

```text
Frame 1 → Person → ID 1
Frame 2 → Person → ID 1
Frame 3 → Person → ID 1
Frame 4 → Person → ID 1
```

This allows the application to understand the movement of individual objects instead of treating every frame as a completely new detection.

### Step 6: Bounding Box and Information

The application draws a bounding box around every tracked object.

The displayed information can include:

```text
Person
ID: 1
Confidence: 0.91
```

The center point of the bounding box is also calculated.

### Step 7: Counting Line

A horizontal virtual line is placed approximately at the center of the video frame.

```text
--------------------------------
          COUNTING LINE
--------------------------------
```

The center point of each tracked object is monitored relative to this line.

### Step 8: IN / OUT Counting

When an object crosses the counting line, its previous and current positions are compared.

If an object moves from above the line to below the line:

```text
Above
  ↓
Line
  ↓
Below
```

it is counted as **IN**.

If an object moves from below the line to above the line:

```text
Below
  ↓
Line
  ↓
Above
```

it is counted as **OUT**.

The application keeps track of already-counted tracking IDs so that the same object is not counted repeatedly.

### Step 9: Processed Video

After detection, tracking, and counting, the processed frame is generated.

The frame contains:

* Bounding boxes
* Object labels
* Confidence scores
* Tracking IDs
* Center points
* Counting line
* IN/OUT information

### Step 10: Web Video Stream

The processed frames are streamed back to the browser through the Flask `/api/video` endpoint.

The user can therefore watch the processed video directly through the web dashboard.

### Step 11: Dashboard Statistics

The frontend periodically requests statistics from:

```text
/api/status
```

The dashboard updates information such as:

```text
Objects: 3
IN: 5
OUT: 2
Status: READY
```

It also displays the detected object classes and their counts.

---

## 🔍 Object Detection

YOLO11 is used to detect objects in every video frame.

For each detected object, the model provides:

* Object class
* Bounding box coordinates
* Confidence score

The bounding box is represented using:

```text
(x1, y1, x2, y2)
```

where:

* `x1` = left coordinate
* `y1` = top coordinate
* `x2` = right coordinate
* `y2` = bottom coordinate

For example:

```text
(x1, y1) ---------------- (x2, y1)
    |                         |
    |         OBJECT          |
    |                         |
(x1, y2) ---------------- (x2, y2)
```

The confidence score represents how confident the model is that the detected object belongs to a particular class.

For example:

```text
Person - 0.94
```

means the model has a confidence score of approximately 94% for that detection.

---

## 🎯 Object Tracking

ByteTrack is used to maintain object identities across consecutive frames.

For example:

```text
Frame 1 → Person → ID 1
Frame 2 → Person → ID 1
Frame 3 → Person → ID 1
Frame 4 → Person → ID 1
```

If another person enters the scene:

```text
Frame 5 → Person → ID 1
Frame 5 → Person → ID 2
```

The tracking IDs allow the application to distinguish between different objects.

Tracking IDs are assigned automatically by the tracking algorithm and are not permanent identities.

---

## 📊 IN / OUT Counting

A horizontal virtual line is placed at the center of the video frame.

```text
-----------------------------  ← Counting Line
```

The center point of every tracked object is calculated.

### IN

When an object moves:

```text
Above the line
      ↓
Crosses the line
      ↓
Below the line
```

it is counted as:

```text
IN
```

### OUT

When an object moves:

```text
Below the line
      ↓
Crosses the line
      ↓
Above the line
```

it is counted as:

```text
OUT
```

The application stores previously counted tracking IDs to prevent counting the same crossing repeatedly.

For example:

```text
ID 1 → crosses line → IN
ID 1 → continues moving → not counted again
```

This prevents duplicate counting for the same object.

---

## 📈 Dashboard

The web dashboard displays the following information.

### Objects

Shows the number of objects detected in the current frame.

Example:

```text
Objects: 4
```

### IN

Shows the total number of objects that crossed the counting line from above to below.

Example:

```text
IN: 5
```

### OUT

Shows the total number of objects that crossed the counting line from below to above.

Example:

```text
OUT: 2
```

### Status

Displays the current processing state, such as:

```text
READY
STARTING
FINISHED
```

### Detection Classes

Displays the number of detected objects grouped by class.

Example:

```text
person      3
car         2
backpack    1
```

---

## 💻 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Lohith-CSE-AIML/Object_Detection.git
```

Move into the project directory:

```bash
cd Object_Detection
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📦 Requirements

The project uses the following Python packages:

```text
Flask
ultralytics
opencv-python
gunicorn
```

These dependencies are also listed in:

```text
requirements.txt
```

---

## ▶️ Run Locally

Start the Flask application:

```bash
python app1.py
```

The application will start locally.

Open the URL shown in the terminal, usually:

```text
http://127.0.0.1:5000
```

---

## 🎥 Using the Application

### Step 1

Open the web application.

### Step 2

Click the video upload field.

### Step 3

Select a video file.

### Step 4

Click:

```text
Start Detection
```

### Step 5

The uploaded video will be processed.

The application will display:

* Bounding boxes
* Object labels
* Confidence scores
* Tracking IDs
* Center points
* Counting line

### Step 6

The dashboard updates the statistics while the video is being processed.

---

## 🔗 Links


* **GitHub Repository:** [Object Detection & Tracking](https://github.com/Lohith-CSE-AIML/CodeAlpha_Object-Detection-and-Tracking-)
* **GitHub Profile:** [Lohith-CSE-AIML](https://github.com/Lohith-CSE-AIML)
* **LinkedIn:** [Thoti Lohith](https://www.linkedin.com/in/thoti-lohith/)


---





---

## 🧩 Important Files

### `app1.py`

The main Flask application.

It handles:

* Flask routes
* Video uploads
* YOLO model loading
* Object detection
* ByteTrack tracking
* IN/OUT counting
* Dashboard statistics
* Video streaming

---

### `object_tracking.py`

Contains the object detection and tracking logic used during development and testing.

---

### `templates/index.html`

Contains the structure of the web dashboard.

It includes:

* Header
* Video upload section
* Detection feed
* Statistics cards
* Detection class list

---

### `static/css/style.css`

Contains the styling of the web dashboard.

It handles:

* Layout
* Colors
* Cards
* Buttons
* Video container
* Responsive design

---

### `static/js/script.js`

Handles frontend interaction.

It:

* Uploads the video to Flask
* Starts the video stream
* Requests dashboard statistics
* Updates object count
* Updates IN/OUT counts
* Updates detection classes
* Updates system status

---

### `yolo11n.pt`

Pretrained YOLO11 Nano model used for object detection.

The model detects common object classes from the pretrained dataset.

---

## 🔄 API Endpoints

### Home

```text
GET /
```

Displays the web dashboard.

---

### Upload Video

```text
POST /upload
```

Uploads and stores the selected video.

---

### Dashboard Status

```text
GET /api/status
```

Returns the current detection statistics.

Example response:

```json
{
    "objects": 2,
    "classes": {
        "person": 2
    },
    "in": 1,
    "out": 0,
    "status": "READY"
}
```

---

### Video Stream

```text
GET /api/video
```

Streams the processed video frames to the web browser.

---

## 🌐 Deployment

The application can be deployed using **Render**.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn app1:app
```

> `app1` refers to the Python file `app1.py`, while `app` refers to the Flask application object created using `Flask(__name__)`.

---

## ⚠️ Limitations

* Detection and tracking performance depends on available CPU resources.
* Processing speed can vary depending on video resolution and length.
* Tracking IDs are not permanent identities.
* Tracking can be affected by heavy occlusion, fast movement, poor lighting, or similar-looking objects.
* The application currently processes one uploaded video at a time.
* The current implementation is designed primarily as a project demonstration rather than a production multi-user system.
* Large video files may require more processing time.
* Free hosting environments may have memory, CPU, execution-time, or inactivity limitations.

---

## 🔮 Future Improvements

Possible future improvements include:

* Webcam/live camera support
* GPU acceleration
* Improved tracking with Deep SORT
* Support for multiple users
* Improved video processing performance
* Object-specific counting
* Configurable counting line
* Downloadable processed videos
* Detection history and analytics
* Database integration
* Authentication and user accounts
* Improved deployment infrastructure

---

## 🎓 Project Objective

The objective of this project is to develop a computer vision system capable of detecting and tracking objects in video streams while providing real-time visualization and movement-based counting.

The project demonstrates the integration of:

```text
Computer Vision
       +
Deep Learning
       +
Object Detection
       +
Object Tracking
       +
Web Development
```

---

## 👨‍💻 Author

**Lohith**

Computer Science Engineering Student

VIT-AP University

* GitHub: [Lohith-CSE-AIML](https://github.com/Lohith-CSE-AIML)
* LinkedIn: [Thoti Lohith](https://www.linkedin.com/in/thoti-lohith/)

---

## 📄 License

This project is intended for educational and demonstration purposes.
