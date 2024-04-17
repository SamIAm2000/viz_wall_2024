

# switched to dlib, works well
# import tkinter as tk
# import cv2
# from PIL import Image, ImageTk
# import math
# import dlib
# import numpy as np

# class MovingWindow:
#     def __init__(self, root, x, y, radius, speed, feature):
#         self.root = root
#         self.x = x
#         self.y = y
#         self.radius = radius
#         self.speed = speed
#         self.angle = 0
#         self.feature = feature
#         self.window = tk.Toplevel()
#         self.window.geometry("320x240")
#         self.canvas = tk.Canvas(self.window, width=320, height=240, bg='white')
#         self.canvas.pack()
#         self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#         self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#     def update_position(self):
#         self.angle += self.speed
#         if self.angle >= 360:
#             self.angle -= 360
#         radians = math.radians(self.angle)
#         new_x = self.x + self.radius * math.cos(radians)
#         new_y = self.y + self.radius * math.sin(radians)
#         self.window.geometry(f"320x240+{int(new_x)}+{int(new_y)}")

#     def detect_faces(self, frame):
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
#         for (x, y, w, h) in faces:
#             # Draw rectangle around face
#             cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
#             # Detect facial landmarks
#             shape = self.predictor(gray, dlib.rectangle(x, y, x+w, y+h))
#             # Convert facial landmarks to numpy array
#             shape = [(p.x, p.y) for p in shape.parts()]
#             shape = np.array(shape, dtype=np.int32)
#             # Detect eyes and mouth
#             left_eye = shape[36:42]
#             right_eye = shape[42:48]
#             mouth = shape[48:68]

#             if self.feature == "left_eye":
#                 self.display_feature(frame, left_eye)
#             elif self.feature == "right_eye":
#                 self.display_feature(frame, right_eye)
#             elif self.feature == "mouth":
#                 self.display_feature(frame, mouth)

#     def display_feature(self, frame, feature_points):
#         # Calculate bounding box for the feature points
#         x, y, w, h = cv2.boundingRect(feature_points)
#         # Draw rectangle around feature
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#         # Zoom in on the feature region
#         feature_img = frame[y:y+h, x:x+w]
#         feature_img = cv2.resize(feature_img, (80, 60))  # Resize to fit window
#         # Convert the frame to PIL Image format
#         image = Image.fromarray(cv2.cvtColor(feature_img, cv2.COLOR_BGR2RGB))
#         # Convert the PIL Image to Tkinter-compatible format
#         photo = ImageTk.PhotoImage(image=image)
#         # Display the image in the middle of the canvas
#         self.canvas.create_image(160, 120, image=photo)
#         self.canvas.image = photo  # To prevent garbage collection

# def update_windows(root, windows):
#     for window in windows:
#         window.update_position()

#     root.after(50, lambda: update_windows(root, windows))

# def update_video(root, windows):
#     for window in windows:
#         ret, frame = window.video_stream.read()
#         if ret:
#             window.detect_faces(frame)
#     root.after(10, lambda: update_video(root, windows))

# def main():
#     root = tk.Tk()
#     root.withdraw()  # Hide the main root window

#     # Create moving windows with video streams for each feature
#     features = ["left_eye", "right_eye", "mouth"]
#     windows = []
#     for i, feature in enumerate(features):
#         window = MovingWindow(root, 300, 300, 200, i + 1, feature)
#         window.video_stream = cv2.VideoCapture(0)
#         window.window.title(feature)
#         windows.append(window)

#     root.after(50, lambda: update_windows(root, windows))
#     root.after(10, lambda: update_video(root, windows))
#     root.mainloop()

# if __name__ == "__main__":
#     main()

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import math
import dlib
import numpy as np

class MovingWindow:
    def __init__(self, root, x, y, radius, speed, feature):
        self.root = root
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = 0
        self.feature = feature
        self.window = tk.Toplevel()
        self.window.geometry("320x240")  # Set window size
        self.canvas = tk.Canvas(self.window, width=320, height=240, bg='white')
        self.canvas.pack()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    def update_position(self):
        self.angle += self.speed
        if self.angle >= 360:
            self.angle -= 360
        radians = math.radians(self.angle)
        new_x = self.x + self.radius * math.cos(radians)
        new_y = self.y + self.radius * math.sin(radians)
        self.window.geometry(f"320x240+{int(new_x)}+{int(new_y)}")  # Update window position

    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            # Detect facial landmarks
            shape = self.predictor(gray, dlib.rectangle(x, y, x+w, y+h))
            # Convert facial landmarks to numpy array
            shape = [(p.x, p.y) for p in shape.parts()]
            shape = np.array(shape, dtype=np.int32)
            # Detect eyes and mouth
            left_eye = shape[36:42]
            right_eye = shape[42:48]
            mouth = shape[48:68]

            if self.feature == "left_eye":
                self.display_feature(frame, left_eye)
            elif self.feature == "right_eye":
                self.display_feature(frame, right_eye)
            elif self.feature == "mouth":
                self.display_feature(frame, mouth)

    def display_feature(self, frame, feature_points):
        # Calculate bounding box for the feature points
        x, y, w, h = cv2.boundingRect(feature_points)

        # Calculate the center point of the bounding rectangle
        center_x = x + w // 2
        center_y = y + h // 2

        # Calculate the top-left corner coordinates of the cropped region
        x = max(0, center_x - 320 // 2)
        y = max(0, center_y - 240 // 2)

        # Calculate the width and height of the cropped region
        width = min(frame.shape[1] - x, 320)
        height = min(frame.shape[0] - y, 240)

        # Crop the region around the feature
        feature_img = frame[y:y+height, x:x+width]
        # Resize the feature image to fit the window while maintaining the aspect ratio
        scale = min(320 / feature_img.shape[1], 240 / feature_img.shape[0])
        feature_img = cv2.resize(feature_img, (int(feature_img.shape[1] * scale), int(feature_img.shape[0] * scale)))
        # # Calculate the position to center the feature image in the window
        # center_x = (320 - feature_img.shape[1]) // 2
        # center_y = (240 - feature_img.shape[0]) // 2
        # Convert the frame to PIL Image format
        image = Image.fromarray(cv2.cvtColor(feature_img, cv2.COLOR_BGR2RGB))
        # Convert the PIL Image to Tkinter-compatible format
        photo = ImageTk.PhotoImage(image=image)
        # Display the image in the canvas
        self.canvas.create_image(0,0, image=photo, anchor="nw")
        self.canvas.image = photo  # To prevent garbage collection

def update_windows(root, windows):
    for window in windows:
        window.update_position()

    root.after(50, lambda: update_windows(root, windows))

def update_video(root, windows):
    for window in windows:
        ret, frame = window.video_stream.read()
        if ret:
            window.detect_faces(frame)
    root.after(10, lambda: update_video(root, windows))

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main root window

    # Create moving windows with video streams for each feature
    features = ["left_eye", "right_eye", "mouth"]
    windows = []
    for i, feature in enumerate(features):
        window = MovingWindow(root, 300, 300, 200, i + 1, feature)
        window.video_stream = cv2.VideoCapture(0)
        window.window.title(feature)
        windows.append(window)

    root.after(50, lambda: update_windows(root, windows))
    root.after(10, lambda: update_video(root, windows))
    root.mainloop()

if __name__ == "__main__":
    main()
