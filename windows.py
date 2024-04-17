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

#     def update_position(self):
#         self.angle += self.speed
#         if self.angle >= 360:
#             self.angle -= 360
#         radians = math.radians(self.angle)
#         new_x = self.x + self.radius * math.cos(radians)
#         new_y = self.y + self.radius * math.sin(radians)
#         self.window.geometry(f"320x240+{int(new_x)}+{int(new_y)}")

# def update_windows(root, windows):
#     for window in windows:
#         window.update_position()

#     root.after(50, lambda: update_windows(root, windows))

# def update_video(root, windows):
#     for window in windows:
#         ret, frame = window.video_stream.read()
#         if ret:
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image = Image.fromarray(frame)
#             photo = ImageTk.PhotoImage(image=image)
#             window.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
#             window.canvas.image = photo  # To prevent garbage collection
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

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import math

class MovingWindow:
    def __init__(self, root, x, y, radius, speed):
        self.root = root
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = 0
        self.window = tk.Toplevel()
        self.window.geometry("320x240")
        self.canvas = tk.Canvas(self.window, width=320, height=240, bg='white')
        self.canvas.pack()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

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
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # Get the face region and convert it to PIL Image format
            face_img = Image.fromarray(frame[y:y+h, x:x+w])
            # Convert the PIL Image to Tkinter-compatible format
            face_tk = ImageTk.PhotoImage(image=face_img)
            # Display the face image in the middle of the canvas
            self.canvas.create_image(160, 120, image=face_tk)
            self.canvas.face_tk = face_tk  # To prevent garbage collection

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

    # Create moving windows with video streams
    windows = []
    for i in range(3):
        window = MovingWindow(root, 300, 300, 200, i + 1)
        window.video_stream = cv2.VideoCapture(0)
        windows.append(window)

    root.after(50, lambda: update_windows(root, windows))
    root.after(10, lambda: update_video(root, windows))
    root.mainloop()

if __name__ == "__main__":
    main()
