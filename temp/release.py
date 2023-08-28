import cv2
import mediapipe as mp

# Initialize MediaPipe Pose module
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize MediaPipe Drawing module for drawing landmarks and connections
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam feed
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR frame to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame for pose estimation
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        # Get landmarks for the hands and head
        right_wrist_landmark = results.pose_landmarks.landmark[
            mp_pose.PoseLandmark.RIGHT_WRIST
        ]
        left_wrist_landmark = results.pose_landmarks.landmark[
            mp_pose.PoseLandmark.LEFT_WRIST
        ]
        head_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]

        # Check if either wrist is above the head
        if (
            right_wrist_landmark.y < head_landmark.y
            or left_wrist_landmark.y < head_landmark.y
        ):
            text = "Release"

            # Calculate text position for top and center of the screen
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 4, 2)[0]
            text_x = (frame.shape[1] - text_size[0]) // 2
            text_y = (
                text_size[1] + 50
            )  # Adjust this value for desired spacing from the top

            cv2.putText(
                frame,
                text,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                4,  # Increased font size for visibility
                (0, 0, 255),
                2,
            )

        # Draw landmarks and connections on the frame
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )

    # Display the frame
    cv2.imshow("Full Body Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
