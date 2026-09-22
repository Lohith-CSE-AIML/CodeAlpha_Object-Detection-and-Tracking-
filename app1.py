from flask import Flask, render_template, Response, request

from ultralytics import YOLO

import cv2 as cv
import os


app = Flask(__name__)


# Upload folder
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Current uploaded video
current_video_path = None


# Load YOLO model
model = YOLO("yolo11n.pt")


# Tracking data
previous_positions = {}

in_ids = set()

out_ids = set()


# Dashboard statistics
current_stats = {
    "objects": 0,
    "classes": {},
    "in": 0,
    "out": 0,
    "status": "READY"
}


print("YOLO model loaded successfully")


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# --------------------------------------------------
# VIDEO UPLOAD
# --------------------------------------------------

@app.route("/upload", methods=["POST"])
def upload_video():

    global current_video_path

    # Check whether video was received
    if "video" not in request.files:

        return {
            "error": "No video selected"
        }, 400


    video = request.files["video"]


    # Check filename
    if video.filename == "":

        return {
            "error": "No video selected"
        }, 400


    # Create video path
    video_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        video.filename
    )


    # Save uploaded video
    video.save(video_path)


    # Store current video path
    current_video_path = video_path


    # ----------------------------------------------
    # RESET PREVIOUS TRACKING DATA
    # ----------------------------------------------

    previous_positions.clear()

    in_ids.clear()

    out_ids.clear()


    # Reset dashboard statistics
    current_stats["objects"] = 0

    current_stats["classes"] = {}

    current_stats["in"] = 0

    current_stats["out"] = 0

    current_stats["status"] = "READY"


    return {
        "message": "Video uploaded successfully"
    }


# --------------------------------------------------
# DASHBOARD STATUS API
# --------------------------------------------------

@app.route("/api/status")
def status():

    return current_stats


# --------------------------------------------------
# GENERATE PROCESSED VIDEO FRAMES
# --------------------------------------------------

def generate_frames():

    global current_video_path


    # No video uploaded
    if current_video_path is None:

        return


    # Open uploaded video
    cap = cv.VideoCapture(current_video_path)


    while True:

        # Read one frame
        ret, frame = cap.read()


        # ------------------------------------------
        # VIDEO FINISHED
        # ------------------------------------------

        if not ret:

            current_stats["status"] = "FINISHED"

            cap.release()

            break


        # ------------------------------------------
        # COUNTING LINE
        # ------------------------------------------

        line_y = frame.shape[0] // 2


        # ------------------------------------------
        # YOLO + BYTE TRACK
        # ------------------------------------------

        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml"
        )


        # ------------------------------------------
        # TOTAL OBJECTS
        # ------------------------------------------

        object_count = len(results[0].boxes)

        current_stats["objects"] = object_count


        # ------------------------------------------
        # CLASS COUNTS
        # ------------------------------------------

        class_counts = {}


        # ------------------------------------------
        # PROCESS EACH DETECTED OBJECT
        # ------------------------------------------

        for box in results[0].boxes:


            # Bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0]


            x1 = int(x1)

            y1 = int(y1)

            x2 = int(x2)

            y2 = int(y2)


            # Class ID
            class_id = int(box.cls[0])


            # Confidence
            confidence = float(box.conf[0])


            # Tracking ID
            if box.id is not None:

                track_id = int(box.id[0])

            else:

                track_id = -1


            # Class name
            class_name = model.names[class_id]


            # --------------------------------------
            # UPDATE CLASS COUNT
            # --------------------------------------

            class_counts[class_name] = (
                class_counts.get(class_name, 0) + 1
            )


            # --------------------------------------
            # CENTER POINT
            # --------------------------------------

            center_x = int((x1 + x2) / 2)

            center_y = int((y1 + y2) / 2)


            # Draw center point
            cv.circle(
                frame,
                (center_x, center_y),
                5,
                (0, 0, 255),
                -1
            )


            # --------------------------------------
            # IN / OUT DETECTION
            # --------------------------------------

            if track_id != -1:


                # Get previous Y position
                previous_y = previous_positions.get(
                    track_id
                )


                # ----------------------------------
                # ABOVE -> BELOW = IN
                # ----------------------------------

                if (
                    previous_y is not None
                    and track_id not in in_ids
                    and previous_y < line_y
                    and center_y >= line_y
                ):

                    current_stats["in"] += 1

                    in_ids.add(track_id)


                # ----------------------------------
                # BELOW -> ABOVE = OUT
                # ----------------------------------

                elif (
                    previous_y is not None
                    and track_id not in out_ids
                    and previous_y > line_y
                    and center_y <= line_y
                ):

                    current_stats["out"] += 1

                    out_ids.add(track_id)


                # Store current position
                previous_positions[track_id] = center_y


            # --------------------------------------
            # DRAW BOUNDING BOX
            # --------------------------------------

            cv.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )


            # --------------------------------------
            # DISPLAY LABEL
            # --------------------------------------

            label = (
                f"ID: {track_id} "
                f"{class_name} "
                f"{confidence:.2f}"
            )


            cv.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )


        # ------------------------------------------
        # DRAW COUNTING LINE
        # ------------------------------------------

        cv.line(
            frame,
            (0, line_y),
            (frame.shape[1], line_y),
            (255, 0, 0),
            2
        )


        # ------------------------------------------
        # UPDATE CLASS STATISTICS
        # ------------------------------------------

        current_stats["classes"] = class_counts


        # ------------------------------------------
        # ENCODE FRAME AS JPEG
        # ------------------------------------------

        ret, buffer = cv.imencode(
            ".jpg",
            frame
        )


        if not ret:

            continue


        frame_bytes = buffer.tobytes()


        # ------------------------------------------
        # SEND FRAME TO BROWSER
        # ------------------------------------------

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )


# --------------------------------------------------
# VIDEO STREAM
# --------------------------------------------------

@app.route("/api/video")
def video():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# --------------------------------------------------
# RUN FLASK
# --------------------------------------------------

if __name__ == "__main__":

    app.run(debug=False)