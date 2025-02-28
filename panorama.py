import cv2
import numpy as np
import os

# Define the file path
video_path = "c:/temp/adtr_jbhifi.mp4"

# Open the video file
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Define the new width and calculate the new height to maintain aspect ratio
new_width = 1000
aspect_ratio = 4320 / 7680
new_height = int(new_width / aspect_ratio)

# Iterate over frame_interval from 2 to 15
for frame_interval in range(2, 16):
    # Iterate over skip_frames from 0.1 to 0.5 seconds
    for skip_time in [0.1, 0.2, 0.3, 0.4, 0.5]:
        # Re-open the video file for each iteration
        cap = cv2.VideoCapture(video_path)
        
        # Skip the initial frames
        fps = cap.get(cv2.CAP_PROP_FPS)
        skip_frames = int(skip_time * fps)
        for _ in range(skip_frames):
            cap.read()

        # Extract frames from the video
        frames = []
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break  # End of video
            if frame_count % frame_interval == 0:
                # Resize the frame to reduce memory usage while maintaining aspect ratio
                frame = cv2.resize(frame, (new_width, new_height))
                frames.append(frame)  # Collect the frame
            frame_count += 1

        cap.release()

        # Check if enough frames were extracted
        print(f"Extracted {len(frames)} frames for frame_interval={frame_interval} and skip_time={skip_time}.")
        if len(frames) < 2:
            result = f"Not enough frames to create a panorama for frame_interval={frame_interval} and skip_time={skip_time}."
            print(result)
        else:
            # Stitch frames into a panoramic image
            stitcher = cv2.Stitcher.create(cv2.Stitcher_SCANS)
            print("Stitching frames...")
            status, panorama = stitcher.stitch(frames)
            print(f"Stitching status: {status}")

            if status == cv2.Stitcher_OK:
                # Apply sharpening to the panorama
                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                panorama = cv2.filter2D(panorama, -1, kernel)

                # Save the panoramic image
                panorama_path = f"c:/temp/panorama_{frame_interval}_{int(skip_time*10)}.jpg"
                cv2.imwrite(panorama_path, panorama)
                result = f"Panorama created successfully: {panorama_path}"
            else:
                result = f"Stitching failed for frame_interval={frame_interval} and skip_time={skip_time}, possibly due to lack of overlap or incompatible frames."
            print(result)
