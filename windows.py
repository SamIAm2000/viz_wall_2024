# import tkinter as tk
# import math

# class MovingWindow:
#     def __init__(self, x, y, radius, speed):
#         self.x = x
#         self.y = y
#         self.radius = radius
#         self.speed = speed
#         self.angle = 0
#         self.window = tk.Toplevel()
#         self.window.geometry("200x200")
#         self.canvas = tk.Canvas(self.window, width=200, height=200, bg='white')
#         self.canvas.pack()
#         self.draw_window()

#     def draw_window(self):
#         self.canvas.create_rectangle(75, 75, 125, 125, fill='blue')

#     def update_position(self):
#         self.angle += self.speed
#         if self.angle >= 360:
#             self.angle -= 360
#         radians = math.radians(self.angle)
#         new_x = self.x + self.radius * math.cos(radians)
#         new_y = self.y + self.radius * math.sin(radians)
#         self.window.geometry(f"200x200+{int(new_x)}+{int(new_y)}")

# def main():
#     root = tk.Tk()
#     root.withdraw()  # Hide the main root window

#     # Create moving windows
#     window1 = MovingWindow(300, 300, 200, 1)
#     window2 = MovingWindow(300, 300, 200, 2)
#     window3 = MovingWindow(300, 300, 200, 3)

#     def update_windows():
#         window1.update_position()
#         window2.update_position()
#         window3.update_position()
#         root.after(50, update_windows)

#     update_windows()
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

    def update_position(self):
        self.angle += self.speed
        if self.angle >= 360:
            self.angle -= 360
        radians = math.radians(self.angle)
        new_x = self.x + self.radius * math.cos(radians)
        new_y = self.y + self.radius * math.sin(radians)
        self.window.geometry(f"320x240+{int(new_x)}+{int(new_y)}")

def update_windows(root, windows):
    for window in windows:
        window.update_position()

    root.after(50, lambda: update_windows(root, windows))

def update_video(root, windows):
    for window in windows:
        ret, frame = window.video_stream.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)
            window.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            window.canvas.image = photo  # To prevent garbage collection
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
