import tkinter as tk
import cv2
from PIL import Image, ImageTk
import math
import dlib
import numpy as np
from tkinter import simpledialog

FEATURE_WINDOW_WIDTH = 320
FEATURE_WINDOW_HEIGHT = 200
FACE_WINDOW_WIDTH = 300
FACE_WINDOW_HEIGHT = 320
FEATURE_SCALE_FACTOR = 3
FACE_SCALE_FACTOR = 0.5


def anonymize_face_pixelate(image, blocks=3):
    # divide the input image into NxN blocks
    (h, w) = image.shape[:2]
    xSteps = np.linspace(0, w, blocks + 1, dtype="int")
    ySteps = np.linspace(0, h, blocks + 1, dtype="int")
    # loop over the blocks in both the x and y direction
    for i in range(1, len(ySteps)):
        for j in range(1, len(xSteps)):
            # compute the starting and ending (x, y)-coordinates
            # for the current block
            startX = xSteps[j - 1]
            startY = ySteps[i - 1]
            endX = xSteps[j]
            endY = ySteps[i]
            # extract the ROI using NumPy array slicing, compute the
            # mean of the ROI, and then draw a rectangle with the
            # mean RGB values over the ROI in the original image
            roi = image[startY:endY, startX:endX]
            (B, G, R) = [int(x) for x in cv2.mean(roi)[:3]]
            cv2.rectangle(image, (startX, startY), (endX, endY),
                          (B, G, R), -1)
    # return the pixelated blurred image
    return image


class MovingWindow:
    def __init__(self, root, x, y, radius, speed, angle, feature, width, height, face=False):
        """
        Initializes a moving window.

        Args:
            root (tk.Tk): The root Tkinter window.
            x (int): The initial x-coordinate of the window.
            y (int): The initial y-coordinate of the window.
            radius (int): The radius of the circular path the window follows.
            speed (int): The speed at which the window moves along the circular path.
            feature (str): The feature to display in the window ("left_eye", "right_eye", "mouth", "nose").
            width (int): The width of the window.
            height (int): The height of the window.
            face (bool): Whether the moving window is a face (default: False).
        """
        self.root = root
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = angle
        self.feature = feature
        self.window = tk.Toplevel()
        self.face = face
        self.width = width
        self.height = height

        self.window.geometry(f"{self.width}x{self.height}")  # Set window size
        self.canvas = tk.Canvas(
            self.window, width=self.width, height=self.height, bg='white')
        self.canvas.pack()
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.predictor = dlib.shape_predictor(
            "shape_predictor_68_face_landmarks.dat")

    def update_position(self):
        """
        Updates the position of the window along the circular path.
        """
        self.angle += self.speed
        if self.angle >= 360:
            self.angle -= 360
        radians = math.radians(self.angle)
        new_x = self.x + self.radius * math.cos(radians)
        new_y = self.y + self.radius * math.sin(radians)
        # Update window position
        self.window.geometry(
            f"{self.width}x{self.height}+{int(new_x)}+{int(new_y)}")

    def detect_faces(self, frame):
        """
        Detects facial features in a video frame and displays the specified feature in the window.

        Args:
            frame (numpy.ndarray): The input video frame.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            # Detect facial landmarks
            shape = self.predictor(gray, dlib.rectangle(x, y, x+w, y+h))
            # Convert facial landmarks to numpy array
            shape = [(p.x, p.y) for p in shape.parts()]
            shape = np.array(shape, dtype=np.int32)
            # Detect eyes, mouth, and nose
            left_eye = shape[36:42]
            right_eye = shape[42:48]
            nose = shape[30:36]
            mouth = shape[48:68]

            if self.feature == "left_eye":
                self.display_feature(frame, left_eye)
            elif self.feature == "right_eye":
                self.display_feature(frame, right_eye)
            elif self.feature == "mouth":
                self.display_feature(frame, mouth)
            elif self.feature == "nose":
                self.display_feature(frame, nose)
            elif self.feature == "face_detection":
                self.display_feature(frame, shape)

    def display_feature(self, frame, feature_points):
        """
        Displays the specified feature in the window.

        Args:
            frame (numpy.ndarray): The input video frame.
            feature_points (numpy.ndarray): The coordinates of the feature points.
        """
        if self.face:
            SCALE_FACTOR = FACE_SCALE_FACTOR
        else:
            SCALE_FACTOR = FEATURE_SCALE_FACTOR

        # Calculate bounding box for the feature points
        x, y, w, h = cv2.boundingRect(feature_points)

        if self.face:
            # Apply Gaussian blur to the face region
            blur_face = anonymize_face_pixelate(frame[y:y+h, x:x+w], blocks=10)
            # cv2.GaussianBlur(frame[y:y+h, x:x+w], (25, 25), 0)

            frame[y:y+h, x:x+w] = blur_face

        # Calculate the center point of the bounding rectangle
        center_x = x + w // 2
        center_y = y + h // 2

        # Calculate the top-left corner coordinates of the cropped region
        x = max(0, center_x - int(self.width / (2 * SCALE_FACTOR)))
        y = max(0, center_y - int(self.height / (2 * SCALE_FACTOR)))

        # Calculate the width and height of the cropped region
        width = min(frame.shape[1] - x, int(self.width / SCALE_FACTOR))
        height = min(frame.shape[0] - y, int(self.height / SCALE_FACTOR))

        # Crop the region around the feature
        feature_img = frame[y:y+height, x:x+width]

        # Resize the feature image to fit the window while maintaining the aspect ratio
        feature_img = cv2.resize(feature_img, (self.width, self.height))
        image = Image.fromarray(cv2.cvtColor(feature_img, cv2.COLOR_BGR2RGB))

        # Convert the PIL Image to Tkinter-compatible format
        photo = ImageTk.PhotoImage(image=image)

        # Display the image in the canvas
        self.canvas.create_image(0, 0, image=photo, anchor="nw")
        self.canvas.image = photo  # To prevent garbage collection


def update_windows(root, windows):
    """
    Updates the position of all windows.

    Args:
        root (tk.Tk): The root Tkinter window.
        windows (list): A list of MovingWindow instances.
    """
    for window in windows:
        window.update_position()

    root.after(50, lambda: update_windows(root, windows))


def update_video(root, windows):
    """
    Updates the video frames in all windows.

    Args:
        root (tk.Tk): The root Tkinter window.
        windows (list): A list of MovingWindow instances.
    """
    for window in windows:
        ret, frame = window.video_stream.read()
        if ret:
            window.detect_faces(frame)
    root.after(10, lambda: update_video(root, windows))


def select_camera():
    root = tk.Tk()
    root.withdraw()  # Hide the main root window
    camera_index = simpledialog.askinteger("Select Camera", "Enter camera index (0 for first camera):", parent=root)
    return camera_index

def main(camera_index):
    """
    Initializes and runs the main application.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main root window

    # Create moving windows with video streams for each feature
    features = ["left_eye", "mouth", "right_eye", "nose"]
    windows = []
    # Get the width and height of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    for i, feature in enumerate(features):
        if feature == "face_detection":
            # Create a moving window for face detection at the center of the screen
            window = MovingWindow(root, screen_width//2 - FACE_WINDOW_WIDTH//2, screen_height//2 -
                                  FACE_WINDOW_HEIGHT//2, 0, 0, 0, feature, FACE_WINDOW_WIDTH, FACE_WINDOW_HEIGHT, face=True)
        else:
            # Create a moving window for each feature at the center of the screen
            window = MovingWindow(root, screen_width//2 - FEATURE_WINDOW_WIDTH//2, screen_height//2 -
                                  FEATURE_WINDOW_HEIGHT//2, 350, 3, 90*i, feature, FEATURE_WINDOW_WIDTH, FEATURE_WINDOW_HEIGHT, face=False)
        window.video_stream = cv2.VideoCapture(camera_index)
        window.window.title(feature)
        windows.append(window)

    root.after(50, lambda: update_windows(root, windows))
    root.after(10, lambda: update_video(root, windows))
    root.mainloop()

if __name__ == "__main__":
    camera_index = select_camera()
    main(camera_index)