import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import numpy as np

class Fitvision(tk.Tk):
    def __init__(self):
        super().__init__()
        self.exercises = ['Lagartijas', 'Sentadillas', 'Escalon', 'Dominadas Pronas', 'Dominadas Supinas']
        self.colors = [{'bg': 'black', 'fg': 'orange'}, {'bg': 'orange', 'fg': 'black'}]
        self.title_font = font.Font(family="Franklin Gothic Medium",size=20)
        self.normal_font = font.Font(family='Microsoft JhengHei', size=16, weight='bold')
        
        self.pose_detector = mp.solutions.pose.Pose(
            static_image_mode=True,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.capture = cv2.VideoCapture(0)
        self.title('Fitvision')
        self.geometry('1280x720')

        self.exercises_canvas = tk.Canvas(self, bg='white')
        self.visualization_canvas = tk.Canvas(self, bg='black',  highlightthickness=0)

        self.exercises_canvas.pack(side=tk.LEFT, fill=tk.BOTH)
        self.visualization_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.exercise_choice = tk.StringVar()
        self.exercise_choice.set('Selecciona un ejercicio')
        self.label_info = tk.Label(self.visualization_canvas, textvariable=self.exercise_choice, font=self.title_font, bg='orange', pady=20, padx=100)
        self.label_info.pack(side=tk.TOP, pady=(0,30))

        self.exercises_title = tk.Label(self.exercises_canvas, text='Lista de ejercicios', font=self.title_font)
        self.exercises_title.pack(side=tk.TOP, fill=tk.X)

        self.video_label = tk.Label(self.visualization_canvas, bg='orange')
        self.video_label.pack(side=tk.TOP)
        self.delay = 1
        self.update()

        for i, exercise in enumerate(self.exercises):
            button = tk.Button(self.exercises_canvas, text=exercise, font=self.normal_font)
            color_scheme = None
            if i % 2 == 0:
                color_scheme = self.colors[0]
            else:
                color_scheme = self.colors[1]
            button.configure(bg=color_scheme['bg'])
            button.configure(fg=color_scheme['fg'])
            button.bind('<Button-1>', self.select_exercise)
            button.pack(side=tk.TOP, fill=tk.BOTH, expand=1.0)

    def select_exercise(self, event):
        text = event.widget.cget('text')
        self.exercise_choice.set(text)

    def calculate_angle(self, hip, knee, heel):
        radians = np.arctan2(knee[1] - hip[1], knee[0] - hip[0]) - np.arctan2(heel[1] - knee[1], heel[0] - knee[0])
        angle = np.abs(np.degrees(radians))
        return angle
    

    def update(self):
        ret, frame = self.capture.read()
        if ret:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.pose_detector.process(rgb)
            if result.pose_landmarks:
                landmarks = result.pose_landmarks.landmark
                selected_exercise = self.exercise_choice.get()
                if selected_exercise == 'Sentadillas':
                    MIN_ANGLE = 100
                    left_hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y * frame.shape[0]]
                    right_hip = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].y * frame.shape[0]]
                    left_knee = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].y * frame.shape[0]]
                    right_knee = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value].y * frame.shape[0]]                
                    left_heel = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HEEL.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.LEFT_HEEL.value].y * frame.shape[0]]
                    right_heel = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HEEL.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HEEL.value].y * frame.shape[0]]
                    left_angle = self.calculate_angle(left_hip, left_knee, left_heel)
                    right_angle = self.calculate_angle(right_hip, right_knee, right_heel)
                    knee_distance = np.abs(left_knee[0] - right_knee[0])
                    if knee_distance > 0.16 * frame.shape[1]:
                        cv2.putText(frame, 'Piernas muy abiertas', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    if left_angle > MIN_ANGLE or right_angle > MIN_ANGLE:
                        cv2.putText(frame, 'Demasiado abajo', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)
                elif selected_exercise == 'Lagartijas':
                    left_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y * frame.shape[0]]
                    right_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y * frame.shape[0]]
                    left_elbow = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].y * frame.shape[0]]
                    right_elbow = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].y * frame.shape[0]]            
                    left_wrist = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y * frame.shape[0]]
                    right_wrist = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].y * frame.shape[0]]
                    left_shoulder_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
                    right_shoulder_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
                    left_ankle = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].y * frame.shape[0]]
                    right_ankle = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].y * frame.shape[0]]
                    feet_distance = np.abs(left_ankle[0] - right_ankle[0])
                    if left_shoulder_elbow_angle < 80 or right_shoulder_elbow_angle < 80:
                        cv2.putText(frame, 'Baja baja baja', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    if feet_distance > 0.05 * frame.shape[1]:
                        cv2.putText(frame, 'Junta las piernas', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                elif selected_exercise == 'Escalon':
                    left_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y * frame.shape[0]]
                    right_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y * frame.shape[0]]
                    left_hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y * frame.shape[0]]
                    right_hip = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].y * frame.shape[0]]
                    torso_angle = self.calculate_angle(left_shoulder, left_hip, right_hip)
                    if torso_angle < 50:
                        cv2.putText(frame, 'Endereza tu torso', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                elif selected_exercise == 'Dominadas Pronas':
                    left_wrist = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y * frame.shape[0]]
                    right_wrist = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].y * frame.shape[0]]
                    wrist_distance = abs(left_wrist[0] - right_wrist[0])
                    if wrist_distance < 170:
                        cv2.putText(frame, 'Separa las manos', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    if wrist_distance > 350:
                        cv2.putText(frame, 'Junta las manos', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    if landmarks[mp.solutions.pose.PoseLandmark.NOSE.value].y * frame.shape[0] > max(left_wrist[1], right_wrist[1]):
                        cv2.putText(frame, 'Sube sube sube', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                elif selected_exercise == 'Dominadas Supinas':
                    left_wrist = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y * frame.shape[0]]
                    right_wrist = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].x * frame.shape[1], landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].y * frame.shape[0]]
                    wrist_distance = abs(left_wrist[0] - right_wrist[0])
                    if wrist_distance < 100:
                        cv2.putText(frame, 'Separa las manos', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    if wrist_distance > 180:
                        cv2.putText(frame, 'Junta las manos', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    if landmarks[mp.solutions.pose.PoseLandmark.NOSE.value].y * frame.shape[0] > max(left_wrist[1], right_wrist[1]):
                        cv2.putText(frame, 'Sube sube sube', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            self.image = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.video_label.config(image=self.image)
        if self.winfo_exists(): 
            self.after(self.delay, self.update)
        else:
            self.capture.release()
            self.pose_detector.close()

fitvision = Fitvision()
fitvision.mainloop()