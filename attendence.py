import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
from tkcalendar import DateEntry
import cv2
import os
import csv
import json
import re
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import time

# === Constants ===
FACE_DIR = "faces"
ATTENDANCE_FILE = "attendance.csv"
USER_CREDENTIALS_FILE = "users.json"

# === Ensure Necessary Files and Directories ===
os.makedirs(FACE_DIR, exist_ok=True)

if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["UID", "Name", "Timestamp"])

if not os.path.exists(USER_CREDENTIALS_FILE):
    with open(USER_CREDENTIALS_FILE, "w") as f:
        json.dump({"admin": "password"}, f)

attendance_today = []
camera_index = 0

# === Initialize App ===
def start_main_app():
    global name_input, uid_input, listbox, app

    app = tk.Tk()
    app.title("Smart Attendance System")
    app.geometry("600x700")
    app.configure(bg="#f9f9f9")

    tk.Label(app, text="Smart Attendance System", font=("Helvetica", 18, "bold"), bg="#f9f9f9").pack(pady=15)

    frame = tk.Frame(app, bg="#f9f9f9")
    frame.pack()

    tk.Label(frame, text="Name:", bg="#f9f9f9").grid(row=0, column=0)
    name_input = tk.Entry(frame, width=30)
    name_input.grid(row=0, column=1, padx=10)

    tk.Label(frame, text="UID:", bg="#f9f9f9").grid(row=1, column=0)
    uid_input = tk.Entry(frame, width=30)
    uid_input.grid(row=1, column=1, padx=10, pady=5)

    btn_frame = tk.Frame(app, bg="#f9f9f9")
    btn_frame.pack()

    tk.Button(btn_frame, text="\ud83d\udcf7 Save Face", command=save_face_image, width=20, bg="#e0f0ff").grid(row=0, column=0, padx=5, pady=5)
    tk.Button(btn_frame, text="\u2705 Mark Attendance", command=recognize_and_log, width=20, bg="#e0ffe0").grid(row=0, column=1, padx=5, pady=5)
    tk.Button(btn_frame, text="\ud83d\udcc4 Export Excel", command=lambda: export_attendance("excel"), bg="#ffe4c4").grid(row=1, column=0, pady=5)
    tk.Button(btn_frame, text="\ud83d\udcc4 Export PDF", command=lambda: export_attendance("pdf"), bg="#ffe4c4").grid(row=1, column=1, pady=5)
    tk.Button(btn_frame, text="\ud83d\udcc1 View Logs", command=view_logs, bg="#f0e0ff", width=20).grid(row=2, column=0, pady=5)
    tk.Button(btn_frame, text="\u2699\ufe0f Admin Panel", command=open_admin_panel, bg="#fff0e0", width=20).grid(row=2, column=1, pady=5)
    tk.Button(btn_frame, text="\u274c Exit", command=app.quit, bg="#ffcccc", width=42).grid(row=3, column=0, columnspan=2, pady=10)

    tk.Label(app, text="Today's Attendance:", font=("Arial", 13, "bold"), bg="#f9f9f9").pack(pady=(15, 5))
    listbox = tk.Listbox(app, width=70, height=10, font=("Courier", 10))
    listbox.pack(padx=30, pady=5)

    app.mainloop()

# === Authentication ===
def authenticate():
    login = tk.Tk()
    login.title("Login")
    login.geometry("300x200")
    login.configure(bg="white")
    login.eval('tk::PlaceWindow . center')

    tk.Label(login, text="Username:", bg="white").pack(pady=(20, 5))
    username_entry = tk.Entry(login)
    username_entry.pack()

    tk.Label(login, text="Password:", bg="white").pack(pady=5)
    password_entry = tk.Entry(login, show="*")
    password_entry.pack()

    def check():
        with open(USER_CREDENTIALS_FILE, "r") as f:
            users = json.load(f)
        if users.get(username_entry.get()) == password_entry.get():
            login.destroy()
            start_main_app()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    tk.Button(login, text="Login", command=check, bg="#e0e0ff").pack(pady=15)
    login.mainloop()

# === Utilities ===
def validate_uid(uid):
    return bool(re.match(r"^\d{2}[A-Za-z]{3}\d{4,5}$", uid))

def validate_name(name):
    return name.replace(" ", "").isalpha()

def already_marked(uid):
    today = datetime.now().strftime("%Y-%m-%d")
    with open(ATTENDANCE_FILE, "r") as file:
        reader = csv.reader(file)
        return any(row[0] == uid and today in row[2] for row in reader if row)

def show_attendance(uid, name, timestamp):
    entry = f"{uid} - {name} at {timestamp}"
    if entry not in attendance_today:
        attendance_today.append(entry)
        listbox.insert(tk.END, entry)

# === Save Face ===
def save_face_image():
    user_name = name_input.get().strip()
    user_uid = uid_input.get().strip()

    if not user_name or not user_uid:
        messagebox.showwarning("Missing Info", "Please enter both Name and UID.")
        return

    if not validate_uid(user_uid):
        messagebox.showwarning("Invalid UID", "UID format is invalid.")
        return

    if not validate_name(user_name):
        messagebox.showwarning("Invalid Name", "Name should only contain alphabets and spaces.")
        return

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Cannot access webcam.")
        return

    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    captured = False
    start = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            if not captured and time.time() - start > 2:
                face = gray[y:y+h, x:x+w]
                filename = f"{FACE_DIR}/{user_uid}_{user_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(filename, face)
                captured = True
                messagebox.showinfo("Captured", f"Face saved: {filename}")
                break

        cv2.putText(frame, f"Capturing {user_name} ({user_uid})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 100), 2)
        cv2.imshow("Face Capture", frame)

        if captured or cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# === Recognize Face and Log ===
def recognize_and_log():
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Cannot access webcam.")
        return

    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    known_faces = {}

    for img in os.listdir(FACE_DIR):
        path = os.path.join(FACE_DIR, img)
        parts = img.split('_')
        if len(parts) >= 2:
            uid, name = parts[0], parts[1]
            image = cv2.imread(path, 0)
            known_faces[img] = (uid, name, image)

    matched = False
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            detected = gray[y:y+h, x:x+w]

            for filename, (uid, name, stored) in known_faces.items():
                try:
                    resized = cv2.resize(detected, (stored.shape[1], stored.shape[0]))
                    result = cv2.matchTemplate(resized, stored, cv2.TM_CCOEFF_NORMED)
                    _, score, _, _ = cv2.minMaxLoc(result)

                    if score > 0.6:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if not already_marked(uid):
                            with open(ATTENDANCE_FILE, "a", newline="") as f:
                                csv.writer(f).writerow([uid, name, timestamp])
                            show_attendance(uid, name, timestamp)
                            messagebox.showinfo("Attendance ✅", f"{name} ({uid}) marked.")
                        else:
                            messagebox.showinfo("Already Marked ⚠️", f"{name} ({uid}) already marked today.")
                        matched = True
                        break
                except Exception as e:
                    print("Matching Error:", e)

            if matched:
                break

        cv2.putText(frame, "Looking for registered faces...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
        cv2.imshow("Attendance Scanner", frame)

        if matched or time.time() - start_time > 8 or cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# === Export Attendance ===
def export_attendance(format="excel"):
    df = pd.read_csv(ATTENDANCE_FILE)
    if format == "excel":
        file = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if file:
            df.to_excel(file, index=False)
            messagebox.showinfo("Exported", f"Exported to {file}")
    else:
        file = filedialog.asksaveasfilename(defaultextension=".pdf")
        if file:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 10, "Attendance Report", ln=True, align="C")
            pdf.ln(10)
            for _, row in df.iterrows():
                pdf.cell(200, 8, f"{row['UID']} - {row['Name']} - {row['Timestamp']}", ln=True)
            pdf.output(file)
            messagebox.showinfo("Exported", f"Exported to {file}")

# === View Logs ===
def view_logs():
    log = tk.Toplevel(app)
    log.title("Attendance Logs")
    log.geometry("600x400")
    log.configure(bg="white")

    cal = DateEntry(log, date_pattern='yyyy-mm-dd')
    cal.pack(pady=5)

    search_entry = tk.Entry(log)
    search_entry.pack(pady=5)

    listbox_logs = tk.Listbox(log, width=80)
    listbox_logs.pack()

    def filter_logs():
        date = cal.get()
        query = search_entry.get().lower()
        listbox_logs.delete(0, tk.END)
        with open(ATTENDANCE_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if date in row[2] or query in row[0].lower() or query in row[1].lower():
                    listbox_logs.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]}")

    tk.Button(log, text="Search Logs", command=filter_logs).pack(pady=5)

# === Admin Panel ===
def open_admin_panel():
    global camera_index
    panel = tk.Toplevel(app)
    panel.title("Admin Panel")
    panel.geometry("300x150")
    panel.configure(bg="white")

    tk.Label(panel, text="Camera Index:", bg="white").pack()
    cam_input = tk.Entry(panel)
    cam_input.insert(0, str(camera_index))
    cam_input.pack()

    def update():
        global camera_index
        try:
            camera_index = int(cam_input.get())
            messagebox.showinfo("Updated", f"Camera set to {camera_index}")
        except:
            messagebox.showerror("Invalid", "Enter a number")

    tk.Button(panel, text="Update", command=update, bg="#e0ffe0").pack(pady=10)

# === Start App ===
authenticate()
