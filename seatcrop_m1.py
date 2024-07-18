import cv2
import os
import csv
from natsort import natsorted
from ultralytics import YOLO
from PIL import Image
from datetime import datetime
import time

# Define the RTSP URLs for the cameras
cameras = {
    "camera1": "rtsp://admin:Nimda@2024@10.10.116.70:554/media/video1",
    "camera2": "rtsp://admin:Nimda@2024@10.10.116.71:554/media/video1",
    "camera3": "rtsp://admin:Nimda@2024@10.10.116.72:554/media/video1",
    "camera4": "rtsp://admin:Nimda@2024@10.10.116.73:554/media/video1",
    "camera5": "rtsp://admin:Nimda@2024@10.10.116.74:554/media/video1",
    "camera6": "rtsp://admin:Nimda@2024@10.10.116.75:554/media/video1"
}

# Paths to the directories and files
roi_folder = "roi_data"
snapshot_base_folder = "snapshots"

# Create the base snapshot folder if it doesn't exist
if not os.path.exists(snapshot_base_folder):
    os.makedirs(snapshot_base_folder)

def create_result_csv(csv_path, result_csv_path):
    # Copy the seat_number and seat_coordinates columns to the result CSV file
    with open(csv_path, mode='r', newline='') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['snapshot', 'status', 'date_time']

        with open(result_csv_path, mode='w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                writer.writerow({field: row[field] for field in fieldnames if field in row})

def update_result_csv(result_csv_path, seatnum, snapshot, status):
    rows = []
    fieldnames = None

    # Read the existing CSV
    with open(result_csv_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        for row in reader:
            if row['seat_number'] == seatnum:
                row[snapshot] = status
                row[snapshot + '_time'] = datetime.now().strftime("%d-%m-%Y %H:%M")
            rows.append(row)

    # If the snapshot column doesn't exist, add it to the fieldnames
    if snapshot not in fieldnames:
        fieldnames.extend([snapshot, snapshot + '_time'])

    # Write back to the CSV
    with open(result_csv_path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def process_image(image_path, csv_path, result_csv_path, snapshot_folder, snapshot_name):
    rois = []
    with open(csv_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            coordinates = eval(row['seat_coordinates'])
            rois.append((row['seat_number'], coordinates))

    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    image_resized = cv2.resize(image, (1661, 750))
    model = YOLO("yolov8x.pt")

    for seatnum, (y1, y2, x1, x2) in rois:
        cropped_image = image_resized[y1:y2, x1:x2]
        cropped_image_path = os.path.join(snapshot_folder, f"{seatnum}_{snapshot_name}.jpg")
        cv2.imwrite(cropped_image_path, cropped_image)

        results = model(cropped_image)
        status = 'Absent'
        for r in results:
            for detection in r.boxes.data:
                if detection[-1] == 0:
                    status = 'Present'
                    break

        update_result_csv(result_csv_path, seatnum, snapshot_name, status)

def capture_and_process(rtsp_url, csv_path, camera_folder, snapshot_counter, result_csv_path):
    snapshot_name = f"snapshot_{snapshot_counter}"
    snapshot_folder = os.path.join(camera_folder, snapshot_name)

    if not os.path.exists(snapshot_folder):
        os.makedirs(snapshot_folder)

    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print(f"Error: Could not open video stream for {camera_folder}")
        return

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print(f"Error: Could not read frame from video stream for {camera_folder}")
        return

    frame_resized = cv2.resize(frame, (1661, 750))
    img_name = os.path.join(snapshot_folder, f"{snapshot_name}.jpg")
    cv2.imwrite(img_name, frame_resized)
    print(f"{img_name} written!")
    
    try:
        process_image(img_name, csv_path, result_csv_path, snapshot_folder, snapshot_name)
    except Exception as e:
        print(f"Error processing image {img_name}: {e}")

def main():
    num_snapshots = 5  # Number of snapshots to capture

    for snapshot_counter in range(1, num_snapshots + 1):
        for camera, rtsp_url in cameras.items():
            camera_folder = os.path.join(snapshot_base_folder, camera)
            if not os.path.exists(camera_folder):
                os.makedirs(camera_folder)

            csv_path = os.path.join(roi_folder, f"roi_{camera}.csv")
            result_csv_path = os.path.join(camera_folder, f"{camera}_res.csv")

            if not os.path.exists(result_csv_path):
                create_result_csv(csv_path, result_csv_path)

            capture_and_process(rtsp_url, csv_path, camera_folder, snapshot_counter, result_csv_path)
            time.sleep(1)  # Wait for 1 second before capturing the next snapshot

if __name__ == "__main__":
    main()
