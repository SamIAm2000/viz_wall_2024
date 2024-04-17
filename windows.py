
#this version centers around faces and tracks faces
# import tkinter as tk
# import cv2
# from PIL import Image, ImageTk
# import math

# class MovingWindow:
#     def __init__(self, root, x, y, radius, speed):
#         self.root = root
#         self.x = x
#         self.y = y
#         self.radius = radius
#         self.speed = speed
#         self.angle = 0
#         self.window = tk.Toplevel()
#         self.window.geometry("320x240")
#         self.canvas = tk.Canvas(self.window, width=320, height=240, bg='white')
#         self.canvas.pack()
#         self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

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
#             cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
#             # Get the face region and convert it to PIL Image format
#             face_img = Image.fromarray(frame[y:y+h, x:x+w])
#             # Convert the PIL Image to Tkinter-compatible format
#             face_tk = ImageTk.PhotoImage(image=face_img)
#             # Display the face image in the middle of the canvas
#             self.canvas.create_image(160, 120, image=face_tk)
#             self.canvas.face_tk = face_tk  # To prevent garbage collection

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

#     # Create moving windows with video streams
#     windows = []
#     for i in range(3):
#         window = MovingWindow(root, 300, 300, 200, i + 1)
#         window.video_stream = cv2.VideoCapture(0)
#         windows.append(window)

#     root.after(50, lambda: update_windows(root, windows))
#     root.after(10, lambda: update_video(root, windows))
#     root.mainloop()

# if __name__ == "__main__":
#     main()

#this version correctly does feature detection, but only displays the top left corner of the video stream
# import tkinter as tk
# import cv2
# from PIL import Image, ImageTk
# import math

# class MovingWindow:
#     def __init__(self, root, x, y, radius, speed):
#         self.root = root
#         self.x = x
#         self.y = y
#         self.radius = radius
#         self.speed = speed
#         self.angle = 0
#         self.window = tk.Toplevel()
#         self.window.geometry("320x240")
#         self.canvas = tk.Canvas(self.window, width=320, height=240, bg='white')
#         self.canvas.pack()
#         self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#         self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
#         self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

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
#             # Get region of interest for eyes and smile
#             roi_gray = gray[y:y+h, x:x+w]
#             roi_color = frame[y:y+h, x:x+w]
#             # Detect eyes
#             eyes = self.eye_cascade.detectMultiScale(roi_gray)
#             for (ex, ey, ew, eh) in eyes:
#                 cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
#             # Detect smile
#             smiles = self.smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)
#             for (sx, sy, sw, sh) in smiles:
#                 cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 2)

#             # Convert the frame to PIL Image format
#             image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
#             # Convert the PIL Image to Tkinter-compatible format
#             photo = ImageTk.PhotoImage(image=image)
#             # Display the image in the Tkinter canvas
#             self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
#             self.canvas.image = photo  # To prevent garbage collection

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

#     # Create moving windows with video streams
#     windows = []
#     for i in range(3):
#         window = MovingWindow(root, 300, 300, 200, i + 1)
#         window.video_stream = cv2.VideoCapture(0)
#         windows.append(window)

#     root.after(50, lambda: update_windows(root, windows))
#     root.after(10, lambda: update_video(root, windows))
#     root.mainloop()

# if __name__ == "__main__":
#     main()

# #facial feature detection works but is wonky
# import tkinter as tk
# import cv2
# from PIL import Image, ImageTk
# import math

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
#         self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
#         self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

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
#             # Get region of interest for eyes and smile
#             roi_gray = gray[y:y+h, x:x+w]
#             roi_color = frame[y:y+h, x:x+w]
#             # Detect eyes
#             eyes = self.eye_cascade.detectMultiScale(roi_gray)
#             # Detect smile
#             smiles = self.smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)
            
#             for (ex, ey, ew, eh) in eyes:
#                 if self.feature == "left_eye" and ex + ew // 2 < w // 2:
#                     # Draw rectangle around eye
#                     cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
#                     # Zoom in on the eye region
#                     eye_img = roi_color[ey:ey+eh, ex:ex+ew]
#                     eye_img = cv2.resize(eye_img, (80, 60))  # Resize to fit window
#                     # Convert the frame to PIL Image format
#                     image = Image.fromarray(cv2.cvtColor(eye_img, cv2.COLOR_BGR2RGB))
#                     # Convert the PIL Image to Tkinter-compatible format
#                     photo = ImageTk.PhotoImage(image=image)
#                     # Display the image in the middle of the canvas
#                     self.canvas.create_image(160, 120, image=photo)
#                     self.canvas.image = photo  # To prevent garbage collection
#                     return
#                 elif self.feature == "right_eye" and ex + ew // 2 > w // 2:
#                     # Draw rectangle around eye
#                     cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
#                     # Zoom in on the eye region
#                     eye_img = roi_color[ey:ey+eh, ex:ex+ew]
#                     eye_img = cv2.resize(eye_img, (80, 60))  # Resize to fit window
#                     # Convert the frame to PIL Image format
#                     image = Image.fromarray(cv2.cvtColor(eye_img, cv2.COLOR_BGR2RGB))
#                     # Convert the PIL Image to Tkinter-compatible format
#                     photo = ImageTk.PhotoImage(image=image)
#                     # Display the image in the middle of the canvas
#                     self.canvas.create_image(160, 120, image=photo)
#                     self.canvas.image = photo  # To prevent garbage collection
#                     return
#             for (sx, sy, sw, sh) in smiles:
#                 if self.feature == "mouth":
#                     # Draw rectangle around smile
#                     cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 2)
#                     # Zoom in on the mouth region
#                     mouth_img = roi_color[sy:sy+sh, sx:sx+sw]
#                     mouth_img = cv2.resize(mouth_img, (80, 60))  # Resize to fit window
#                     # Convert the frame to PIL Image format
#                     image = Image.fromarray(cv2.cvtColor(mouth_img, cv2.COLOR_BGR2RGB))
#                     # Convert the PIL Image to Tkinter-compatible format
#                     photo = ImageTk.PhotoImage(image=image)
#                     # Display the image in the middle of the canvas
#                     self.canvas.create_image(160, 120, image=photo)
#                     self.canvas.image = photo  # To prevent garbage collection
#                     return

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


# switched to dlib, works well
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
        self.window.geometry("320x240")
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
        self.window.geometry(f"320x240+{int(new_x)}+{int(new_y)}")

    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
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
        # Draw rectangle around feature
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # Zoom in on the feature region
        feature_img = frame[y:y+h, x:x+w]
        feature_img = cv2.resize(feature_img, (80, 60))  # Resize to fit window
        # Convert the frame to PIL Image format
        image = Image.fromarray(cv2.cvtColor(feature_img, cv2.COLOR_BGR2RGB))
        # Convert the PIL Image to Tkinter-compatible format
        photo = ImageTk.PhotoImage(image=image)
        # Display the image in the middle of the canvas
        self.canvas.create_image(160, 120, image=photo)
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
