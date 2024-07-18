# import cv2
# import os
# import csv
# from natsort import natsorted
# from ultralytics import YOLO
# from PIL import Image
# from datetime import datetime
# import time
# import glob

# # Define the RTSP URLs for the cameras
# cameras = {
#     "camera1": "rtsp://dd:Lbsnaa123@10.10.116.67",
#     "camera2": "rtsp://dd:Lbsnaa123@10.10.116.67",
#     # "camera3": "rtsp://dd:Lbsnaa123@10.10.116.67",
#     # "camera4": "rtsp://admin:Lbsnaa@123@10.10.116.66:554/media/video1",
#     # "camera5": "rtsp://dd:Lbsnaa123@10.10.116.67",
#     # "camera6": "rtsp://admin:Lbsnaa@123@10.10.116.66:554/media/video1"
# }

# # Paths to the directories and files
# roi_folder = "roi_data"
# snapshot_base_folder = "snapshots"

# # Create the base snapshot folder if it doesn't exist
# if not os.path.exists(snapshot_base_folder):
#     os.makedirs(snapshot_base_folder)

# def create_result_csv(csv_path, result_csv_path):
#     # Copy the seat_number and seat_coordinates columns to the result CSV file
#     with open(csv_path, mode='r', newline='') as infile:
#         reader = csv.DictReader(infile)
#         fieldnames = reader.fieldnames + ['status', 'date_time']

#         with open(result_csv_path, mode='w', newline='') as outfile:
#             writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#             writer.writeheader()
#             for row in reader:
#                 row['status'] = 'Absent'
#                 row['date_time'] = ''
#                 writer.writerow(row)

# def update_result_csv(result_csv_path, seatnum, status):
#     rows = []
#     with open(result_csv_path, mode='r', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         fieldnames = reader.fieldnames

#         for row in reader:
#             if row['seat_number'] == seatnum:
#                 row['status'] = status
#                 row['date_time'] = datetime.now().strftime("%d-%m-%Y %H:%M")
#             rows.append(row)

#     with open(result_csv_path, mode='w', newline='') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(rows)

# def process_image(image_path, csv_path, result_csv_path):
#     class_name = os.path.basename(image_path).split('.')[0]
#     result_folder = os.path.dirname(result_csv_path)

#     rois = []
#     with open(csv_path, mode='r') as csvfile:
#         reader = csv.DictReader(csvfile)
#         headers = reader.fieldnames

#         for row in reader:
#             coordinates = eval(row['seat_coordinates'])
#             rois.append((row['seat_number'], coordinates))

#     image = cv2.imread(image_path)
#     if image is None:
#         raise FileNotFoundError(f"Image not found at {image_path}")

#     # Resize the image to 1661 x 750 as done during ROI definition
#     image_resized = cv2.resize(image, (1661, 750))

#     for seatnum, (y1, y2, x1, x2) in rois:
#         cropped_image = image_resized[y1:y2, x1:x2]
#         outfile = os.path.join(result_folder, seatnum + ".jpg")
#         cv2.imwrite(outfile, cropped_image)

#     model = YOLO("yolov8x.pt")

#     image_files = natsorted(glob.glob(os.path.join(result_folder, "*.jpg")))

#     imgs = [cv2.imread(file) for file in image_files]
#     if not imgs or any(img is None for img in imgs):
#         raise ValueError("No valid images found to process.")

#     results = model.predict(imgs, save=True, save_txt=True, project=result_folder, name='results', exist_ok=True)

#     for i, r in enumerate(results):
#         im_bgr = r.plot()
#         im_rgb = Image.fromarray(im_bgr[..., ::-1])
#         result_filename = f"results{i}.jpg"
#         result_path = os.path.join(result_folder, result_filename)
#         r.save(filename=result_path)

#         seatnum = os.path.basename(image_files[i]).split('.')[0]
#         status = 'Absent'
#         for detection in r.boxes.data:
#             if detection[-1] == 0:
#                 status = 'Present'
#                 break
#         update_result_csv(result_csv_path, seatnum, status)

# def capture_and_process(rtsp_url, csv_path, snapshot_folder, img_counter, result_csv_path):
#     cap = cv2.VideoCapture(rtsp_url)
#     if not cap.isOpened():
#         print(f"Error: Could not open video stream for {snapshot_folder}")
#         return img_counter

#     ret, frame = cap.read()
#     cap.release()

#     if not ret:
#         print(f"Error: Could not read frame from video stream for {snapshot_folder}")
#         return img_counter

#     # Resize the frame to 1661 x 750 as done during ROI definition
#     frame_resized = cv2.resize(frame, (1661, 750))

#     img_name = os.path.join(snapshot_folder, f"snapshot_{img_counter}.jpg")
#     cv2.imwrite(img_name, frame_resized)
#     print(f"{img_name} written!")
#     try:
#         process_image(img_name, csv_path, result_csv_path)
#     except Exception as e:
#         print(f"Error processing image {img_name}: {e}")

#     img_counter += 1
#     return img_counter

# def main():
#     num_snapshots = 2  # Number of snapshots to capture

#     for i in range(num_snapshots):
#         for camera, rtsp_url in cameras.items():
#             camera_folder = os.path.join(snapshot_base_folder, camera)
#             if not os.path.exists(camera_folder):
#                 os.makedirs(camera_folder)

#             csv_path = os.path.join(roi_folder, f"roi_{camera}.csv")
#             result_csv_path = os.path.join(camera_folder, f"{camera}_res.csv")

#             if not os.path.exists(result_csv_path):
#                 create_result_csv(csv_path, result_csv_path)

#             img_counter = 0
#             img_counter = capture_and_process(rtsp_url, csv_path, camera_folder, img_counter, result_csv_path)
#             time.sleep(60)  # Wait for 1 second before capturing the next snapshot

# if __name__ == "__main__":
#     main()
import cv2
import os
import csv
from natsort import natsorted
from ultralytics import YOLO
from PIL import Image
from datetime import datetime
import time

# # Define the RTSP URLs for the cameras
# cameras = {
#     "camera1": "rtsp://dd:Lbsnaa123@10.10.116.67",
#     "camera2": "rtsp://dd:Lbsnaa123@10.10.116.67",
#     # "camera3": "rtsp://dd:Lbsnaa123@10.10.116.67",
#     # "camera4": "rtsp://admin:Lbsnaa@123@10.10.116.66:554/media/video1",
#     # "camera5": "rtsp://dd:Lbsnaa123@10.10.116.67",
#     # "camera6": "rtsp://admin:Lbsnaa@123@10.10.116.66:554/media/video1"
# }
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
        fieldnames = reader.fieldnames + ['status', 'date_time']

        with open(result_csv_path, mode='w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                row['status'] = 'Absent'
                row['date_time'] = ''
                writer.writerow(row)

def update_result_csv(result_csv_path, seatnum, status):
    rows = []
    with open(result_csv_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames

        for row in reader:
            if row['seat_number'] == seatnum:
                row['status'] = status
                row['date_time'] = datetime.now().strftime("%d-%m-%Y %H:%M")
            rows.append(row)

    with open(result_csv_path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def process_image(image_path, csv_path, result_csv_path):
    class_name = os.path.basename(image_path).split('.')[0]
    result_folder = os.path.dirname(result_csv_path)

    rois = []
    with open(csv_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames

        for row in reader:
            coordinates = eval(row['seat_coordinates'])
            rois.append((row['seat_number'], coordinates))

    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # Resize the image to 1661 x 750 as done during ROI definition
    image_resized = cv2.resize(image, (1661, 750))

    model = YOLO("yolov8x.pt")

    # Process each ROI separately
    for seatnum, (y1, y2, x1, x2) in rois:
        cropped_image = image_resized[y1:y2, x1:x2]
        outfile = os.path.join(result_folder, seatnum + ".jpg")
        cv2.imwrite(outfile, cropped_image)

        # Predict using YOLO on the cropped image
        results = model(cropped_image)

        # Determine the status
        status = 'Absent'
        for r in results:
            for detection in r.boxes.data:
                if detection[-1] == 0:  # Assuming class 0 is the 'person' class
                    status = 'Present'
                    break

        # Update the result CSV with the status
        update_result_csv(result_csv_path, seatnum, status)

        # Save the detection result image
        im_bgr = results[0].plot()
        im_rgb = Image.fromarray(im_bgr[..., ::-1])
        result_filename = f"{seatnum}_result.jpg"
        result_path = os.path.join(result_folder, result_filename)
        results[0].save(filename=result_path)

def capture_and_process(rtsp_url, csv_path, snapshot_folder, img_counter, result_csv_path):
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print(f"Error: Could not open video stream for {snapshot_folder}")
        return img_counter

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print(f"Error: Could not read frame from video stream for {snapshot_folder}")
        return img_counter

    # Resize the frame to 1661 x 750 as done during ROI definition
    frame_resized = cv2.resize(frame, (1661, 750))

    img_name = os.path.join(snapshot_folder, f"snapshot_{img_counter}.jpg")
    cv2.imwrite(img_name, frame_resized)
    print(f"{img_name} written!")
    try:
        process_image(img_name, csv_path, result_csv_path)
    except Exception as e:
        print(f"Error processing image {img_name}: {e}")

    img_counter += 1
    return img_counter

def main():
    num_snapshots = 5  # Number of snapshots to capture

    for i in range(num_snapshots):
        for camera, rtsp_url in cameras.items():
            camera_folder = os.path.join(snapshot_base_folder, camera)
            if not os.path.exists(camera_folder):
                os.makedirs(camera_folder)

            csv_path = os.path.join(roi_folder, f"roi_{camera}.csv")
            result_csv_path = os.path.join(camera_folder, f"{camera}_res.csv")

            if not os.path.exists(result_csv_path):
                create_result_csv(csv_path, result_csv_path)

            img_counter = 0
            img_counter = capture_and_process(rtsp_url, csv_path, camera_folder, img_counter, result_csv_path)
            time.sleep(1)  # Wait for 1 second before capturing the next snapshot

if __name__ == "__main__":
    main()
