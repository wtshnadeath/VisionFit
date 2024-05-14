import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import cv2

class Fitvision(tk.Tk):
    def __init__(self):
        super().__init__()

        exercises = ['Lagartijas', 'Sentadillas', 'Escalon', 'Dominadas Pronas', 'Dominadas Supinas']
        colors = [{'bg': 'lightgrey', 'fg': 'black'}, {'bg': 'grey', 'fg': 'white'}]
        title_font = font.Font(family="Franklin Gothic Medium",size=20)
        normal_font = font.Font(family='Microsoft JhengHei', size=16, weight='bold')
        
        self.capture = cv2.VideoCapture(0)
        self.title('Fitvision')
        self.geometry('1280x720')

        self.exercises_canvas = tk.Canvas(self, bg='white')
        self.visualization_canvas = tk.Canvas(self, bg='lightgray')

        self.exercises_canvas.pack(side=tk.LEFT, fill=tk.BOTH)
        self.visualization_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        self.exercises_title = tk.Label(self.exercises_canvas, text='Lista de ejercicios', font=title_font)
        self.exercises_title.pack(side=tk.TOP, fill=tk.X)

        self.video_label = tk.Label(self.visualization_canvas)
        self.video_label.pack(side=tk.TOP)
        self.delay = 1
        self.update()

        self.label_info = tk.Label(self.visualization_canvas, text='Correcto/Incorrecto', font=title_font, bg='lightgreen')
        self.label_info.pack(side=tk.BOTTOM)
    
        for i, exercise in enumerate(exercises):
            button = tk.Button(self.exercises_canvas, text=exercise, font=normal_font)
            color_scheme = None
            if i % 2 == 0:
                color_scheme = colors[0]
            else:
                color_scheme = colors[1]
            button.configure(bg=color_scheme['bg'])
            button.configure(fg=color_scheme['fg'])
            button.pack(side=tk.TOP, fill=tk.BOTH, expand=1.0)

    def update(self):
        ret, frame = self.capture.read()
        if ret:
            self.image = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.video_label.config(image=self.image)
        self.after(self.delay, self.update)

fitvision = Fitvision()
fitvision.mainloop()
