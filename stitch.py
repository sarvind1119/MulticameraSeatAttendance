# import cv2
# import numpy as np

# # List of RTSP URLs
# rtsp_urls = [
#     "rtsp://admin:Nimda@2024@10.10.116.70:554/media/video1",
#     "rtsp://admin:Nimda@2024@10.10.116.75:554/media/video1",
#     # "rtsp://camera3_url",
#     # "rtsp://camera4_url",
#     # "rtsp://camera5_url",
#     # "rtsp://camera6_url"
# ]

# # Open the camera streams
# caps = [cv2.VideoCapture(url) for url in rtsp_urls]

# while True:
#     frames = []
#     for cap in caps:
#         ret, frame = cap.read()
#         if ret:
#             frames.append(frame)

#     if len(frames) == 6:
#         # Example of horizontal stacking (can be adjusted as needed)
#         top_row = np.hstack(frames[:3])
#         bottom_row = np.hstack(frames[3:])
#         combined_frame = np.vstack([top_row, bottom_row])

#         # Display the combined frame
#         cv2.imshow('Combined Frame', combined_frame)

#         # Break the loop on 'q' key press
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# # Release the video captures and destroy windows
# for cap in caps:
#     cap.release()
# cv2.destroyAllWindows()


"""Steps Explanation:
1.Capture the RTSP Feeds: We open each RTSP feed using cv2.VideoCapture().
2.Stitch the Feeds Together: We read frames from each feed and horizontally and vertically stack them to create a single composite frame.
3.Display the Combined Frame: The combined frame is displayed, and you can then proceed to mark the ROIs.
Enhancements:
4.Dynamic Layout: Adjust the layout of the combined feed based on the camera positions in the classroom.
5.Error Handling: Add error handling to manage feed interruptions or quality issues.
Optimization: Optimize the stitching process for real-time performance."""

# import cv2
# import numpy as np

# # List of RTSP URLs for the two cameras
# rtsp_urls = [
#     "rtsp://admin:Nimda@2024@10.10.116.70:554/media/video1",
#     "rtsp://admin:Nimda@2024@10.10.116.75:554/media/video1"
# ]

# # Open the camera streams
# caps = [cv2.VideoCapture(url) for url in rtsp_urls]

# while True:
#     frames = []
#     for cap in caps:
#         ret, frame = cap.read()
#         if ret:
#             frames.append(frame)

#     if len(frames) == 2:
#         # Horizontal stacking of the two frames
#         combined_frame = np.hstack(frames)

#         # Display the combined frame
#         cv2.imshow('Combined Frame', combined_frame)

#         # Break the loop on 'q' key press
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# # Release the video captures and destroy windows
# for cap in caps:
#     cap.release()
# cv2.destroyAllWindows()
# import cv2
# import numpy as np

# # List of RTSP URLs for the six cameras
# rtsp_urls = [
#     "rtsp://admin:Nimda@2024@10.10.116.70:554/media/video1",
#     "rtsp://admin:Nimda@2024@10.10.116.71:554/media/video1",
#     "rtsp://admin:Nimda@2024@10.10.116.72:554/media/video1",
#     "rtsp://admin:Nimda@2024@10.10.116.73:554/media/video1",
#     "rtsp://admin:Nimda@2024@10.10.116.74:554/media/video1",
#     "rtsp://admin:Nimda@2024@10.10.116.75:554/media/video1"
# ]

# # Open the camera streams with buffer size setting
# caps = []
# for url in rtsp_urls:
#     cap = cv2.VideoCapture(url)
#     cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)  # Increase buffer size
#     caps.append(cap)

# while True:
#     frames = []
#     for cap in caps:
#         ret, frame = cap.read()
#         if ret:
#             frames.append(frame)

#     if len(frames) == 6:
#         # Example layout for a 2x3 grid
#         top_row = np.hstack(frames[:3])
#         bottom_row = np.hstack(frames[3:])
#         combined_frame = np.vstack([top_row, bottom_row])

#         # Resize the combined frame to 1600x1200
#         resized_frame = cv2.resize(combined_frame, (1600, 1200))

#         # Display the resized combined frame
#         cv2.imshow('Combined Frame', resized_frame)

#         # Break the loop on 'q' key press
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# # Release the video captures and destroy windows
# for cap in caps:
#     cap.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np

# List of RTSP URLs for the six cameras
rtsp_urls = [
    "rtsp://admin:Nimda@2024@10.10.116.70:554/media/video1",
    "rtsp://admin:Nimda@2024@10.10.116.71:554/media/video1",
    "rtsp://admin:Nimda@2024@10.10.116.72:554/media/video1",
    "rtsp://admin:Nimda@2024@10.10.116.73:554/media/video1",
    "rtsp://admin:Nimda@2024@10.10.116.74:554/media/video1",
    "rtsp://admin:Nimda@2024@10.10.116.75:554/media/video1"
]

# Desired width and height for all frames
desired_width = 500
desired_height = 350

# Open the camera streams with buffer size setting
caps = []
for url in rtsp_urls:
    cap = cv2.VideoCapture(url)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 20)  # Increase buffer size
    caps.append(cap)

def resize_frame(frame, width, height):
    """Resize frame to the given width and height."""
    return cv2.resize(frame, (width, height))

while True:
    frames = []
    for cap in caps:
        ret, frame = cap.read()
        if ret:
            resized_frame = resize_frame(frame, desired_width, desired_height)
            frames.append(resized_frame)

    if len(frames) == 6:
        # Example layout for a 2x3 grid
        top_row = np.hstack(frames[:3])
        bottom_row = np.hstack(frames[3:])
        combined_frame = np.vstack([top_row, bottom_row])

        # Resize the combined frame to 1600x1200
        resized_combined_frame = cv2.resize(combined_frame, (1600, 1200))

        # Display the resized combined frame
        cv2.imshow('Combined Frame', resized_combined_frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video captures and destroy windows
for cap in caps:
    cap.release()
cv2.destroyAllWindows()


