import cv2
import mediapipe
import pyautogui
import time

face_mesh_landmarks = mediapipe.solutions.face_mesh.FaceMesh(refine_landmarks=True)
cam = cv2.VideoCapture(0)

# Set lower resolution for the camera
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 240)  # Set width to 640 pixels
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # Set height to 480 pixels

screen_w, screen_h = pyautogui.size()
click_held = False
t1 = cv2.getTickCount()
frame_counter = 0

while True:
    _, image = cam.read()
    image = cv2.flip(image, 1)
    window_h, window_w, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    processed_image = face_mesh_landmarks.process(rgb_image)
    all_face_landmark_points = processed_image.multi_face_landmarks

    # Monitor framerate
    freq = cv2.getTickFrequency()

    if all_face_landmark_points and frame_counter % 2 == 0:  # Process every 2nd frame
        one_face_landmark_points = all_face_landmark_points[0].landmark
        left_eye = [one_face_landmark_points[145], one_face_landmark_points[159]]

        for landmark_point in left_eye:
            x = int(landmark_point.x * window_w)
            y = int(landmark_point.y * window_h)
            cv2.circle(image, (x, y), 3, (0, 255, 255))

        if (left_eye[0].y - left_eye[1].y < 0.01):
            if not click_held:
                pyautogui.mouseDown()
                click_held = True
        else:
            if click_held:
                pyautogui.mouseUp()
                click_held = False

        for id, landmark_point in enumerate(one_face_landmark_points[474:478]):
            x = int(landmark_point.x * window_w)
            y = int(landmark_point.y * window_h)
            if id == 1:
                mouse_x = int(screen_w / window_w * x)
                mouse_y = int(screen_h / window_h * y)
                pyautogui.moveTo(mouse_x, mouse_y)

    # Calculate framerate
    t2 = cv2.getTickCount()
    time1 = (t2 - t1) / freq
    frame_rate_calc = 1 / time1

    # Display FPS on the image
    cv2.putText(image, "FPS: " + str(int(frame_rate_calc)), (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Eye Controlled Mouse", image)

    t1 = t2
    frame_counter += 1  # Increment frame counter
    key = cv2.waitKey(1)  # Reduced wait time for smoother performance
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()
