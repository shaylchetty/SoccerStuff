# Example using OpenPose Python API
import cv2
import os
from openpose import pyopenpose as op

# Specify OpenPose parameters
params = {
    "model_folder": "path_to_openpose_models",
    "net_resolution": "-1x368",  # Adjust the resolution as needed
    "number_people_max": 10,     # Maximum number of people to detect
}

# Initialize OpenPose
openpose = op.WrapperPython()
openpose.configure(params)
openpose.start()

# Load and process an image
image = cv2.imread('soccer_field.jpg')
datum = op.Datum()
datum.cvInputData = image
openpose.emplaceAndPop([datum])

# Process pose keypoints
keypoints = datum.poseKeypoints

# Visualize keypoints on the image
if len(keypoints) > 0:
    for person_keypoints in keypoints:
        for keypoint in person_keypoints:
            if keypoint[2] > 0:  # Check if keypoint is detected
                x, y = int(keypoint[0]), int(keypoint[1])
                cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

# Display the result
cv2.imshow('Pose Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
