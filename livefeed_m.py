# import cv2
# import os

# # Define the RTSP URLs for the cameras
# camera_urls = {
#     1: "rtsp://dd:Lbsnaa123@10.10.116.67",
#     2: "rtsp://dd:Lbsnaa123@10.10.116.67",
#     #3: "rtsp://dd:Lbsnaa123@10.10.116.67",
#     #4: "rtsp://admin:Lbsnaa@123@10.10.116.66:554/media/video1",
#     #5: "rtsp://example.com/camera5",
#     #6: "rtsp://example.com/camera6"
# }

# def save_image(camera_id, url):
#     folder_name = f"snapshots/camera{camera_id}"
#     if not os.path.exists(folder_name):
#         os.makedirs(folder_name)

#     cap = cv2.VideoCapture(url)
#     ret, frame = cap.read()
#     if ret:
#         image_path = os.path.join(folder_name, "snapshot.png")
#         cv2.imwrite(image_path, frame)
#         print(f"Image saved for camera {camera_id} at {image_path}")
#     else:
#         print(f"Failed to capture image for camera {camera_id}")

#     cap.release()

# def main():
#     while True:
#         for camera_id, url in camera_urls.items():
#             user_input = input(f"Do you want to save an image for camera {camera_id}? (y/n/q): ").strip().lower()
#             if user_input == 'y':
#                 save_image(camera_id, url)
#             elif user_input == 'q':
#                 print("Exiting the program.")
#                 return
#             elif user_input != 'n':
#                 print("Invalid input, please enter 'y', 'n', or 'q'.")

# if __name__ == "__main__":
#     main()
import cv2
import os

# Define the RTSP URLs for the cameras
camera_urls = {
    1: "rtsp://admin:Nimda@2024@10.10.116.70:554/media/video1",
    2: "rtsp://admin:Nimda@2024@10.10.116.71:554/media/video1",
    3: "rtsp://admin:Nimda@2024@10.10.116.72:554/media/video1",
    4: "rtsp://admin:Nimda@2024@10.10.116.73:554/media/video1",
    5: "rtsp://admin:Nimda@2024@10.10.116.74:554/media/video1",
    6: "rtsp://admin:Nimda@2024@10.10.116.75:554/media/video1"
}

def save_image(camera_id, url):
    folder_name = f"snapshots/camera{camera_id}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    cap = cv2.VideoCapture(url)
    ret, frame = cap.read()
    if ret:
        # Resize the image to the specified resolution
        resized_frame = cv2.resize(frame, (1400,900))
        image_path = os.path.join(folder_name, "snapshot.png")
        cv2.imwrite(image_path, resized_frame)
        print(f"Image saved for camera {camera_id} at {image_path}")
    else:
        print(f"Failed to capture image for camera {camera_id}")

    cap.release()

def main():
    while True:
        for camera_id, url in camera_urls.items():
            user_input = input(f"Do you want to save an image for camera {camera_id}? (y/n/q): ").strip().lower()
            if user_input == 'y':
                save_image(camera_id, url)
            elif user_input == 'q':
                print("Exiting the program.")
                return
            elif user_input != 'n':
                print("Invalid input, please enter 'y', 'n', or 'q'.")

if __name__ == "__main__":
    main()
