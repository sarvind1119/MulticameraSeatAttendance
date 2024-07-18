import cv2
import os
import csv

def define_rois(image_path, csv_path):
    """
    Allows user to define multiple Regions of Interest (ROIs) on the image.
    User can enter seat number for each ROI and continue until they choose to quit.
    """
    image = cv2.imread(image_path)
    # Resize the frame to 1661 x 750
    frame_resized = cv2.resize(image, (1661, 750))
    
    # Display the resulting frame
    cv2.imshow('Video Stream', frame_resized)
    rois = []

    # Open CSV file in append mode
    with open(csv_path, mode='a', newline='') as csvfile:
        fieldnames = ['seat_number', 'seat_coordinates', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # If file is empty, write the header
        if csvfile.tell() == 0:
            writer.writeheader()

        seat_numbers = set()

        while True:
            # Ask for seat number
            seatnum = input('Enter seat number (or "q" to quit, "new" to switch camera): ')
            if seatnum.lower() == 'q':
                break
            elif seatnum.lower() == 'new':
                return 'new'

            if seatnum in seat_numbers:
                print("Seat number already exists. Please enter a different seat number.")
                continue

            # Select ROI
            r = cv2.selectROI("Select the area", frame_resized, fromCenter=False, showCrosshair=True)

            # If a valid ROI is selected, add it to the list and save to CSV
            if r[2] > 0 and r[3] > 0:
                coordinates = [int(r[1]), int(r[1] + r[3]), int(r[0]), int(r[0] + r[2])]
                rois.append((seatnum, coordinates))
                writer.writerow({'seat_number': seatnum, 'seat_coordinates': coordinates})
                seat_numbers.add(seatnum)

                # Crop image and save it
                cropped_image = image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
                outfile = os.path.join(os.path.dirname(image_path), "seats", f"{seatnum}.jpg")
                if not os.path.exists(os.path.dirname(outfile)):
                    os.makedirs(os.path.dirname(outfile))
                cv2.imwrite(outfile, cropped_image)
                print(f"Saved cropped image to: {outfile}")

            cv2.destroyWindow("Select the area")

    return 'continue'

def main():
    base_folder = "snapshots"
    camera_folders = [f"camera{i}" for i in range(1, 7)]

    while True:
        camera_choice = input(f"For which camera do you want to mark ROI? (1-{len(camera_folders)}, or 'q' to quit): ").strip()
        if camera_choice.lower() == 'q':
            break

        try:
            camera_index = int(camera_choice)
            if camera_index < 1 or camera_index > len(camera_folders):
                print("Invalid camera choice. Please try again.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number corresponding to the camera or 'q' to quit.")
            continue

        folder_path = os.path.join(base_folder, f"camera{camera_index}")
        if not os.path.exists(folder_path):
            print(f"Folder {folder_path} does not exist.")
            continue

        image_path = os.path.join(folder_path, "snapshot.png")
        if not os.path.isfile(image_path):
            print(f"No image found in {folder_path}.")
            continue

        roi_file = os.path.join(folder_path, f"roi_camera{camera_index}.csv")
        result = define_rois(image_path, roi_file)
        if result == 'new':
            continue
        elif result == 'continue':
            continue
        else:
            break

if __name__ == "__main__":
    main()
