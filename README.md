# Smart Attendance System 👁️‍🗨️✅

A Python-based Face Recognition Attendance System using OpenCV and Tkinter GUI. This project allows users to register faces, recognize them through the webcam, and mark attendance, which can be exported in Excel or PDF format.

## 📌 Features

- 🧑‍💼 **Login System** – Secure login for admin access
- 📸 **Face Registration** – Capture face using webcam and associate with UID & Name
- 🎯 **Face Recognition** – Identify registered faces in real-time
- ✅ **Mark Attendance** – Automatically logs UID, Name, and Timestamp
- 📁 **Attendance Logs** – View attendance by date or person
- 📤 **Export Data** – Export attendance records in Excel or PDF
- ⚙️ **Admin Panel** – Set camera index, manage configurations

---

## 🖼️ GUI Overview

- Login Page appears on startup
- Upon successful login, the Attendance System dashboard loads
- User-friendly layout with buttons for key actions

---

## 💻 Technologies Used

- Python 3.x
- OpenCV
- Tkinter
- Pandas
- FPDF
- tkcalendar

---

## 📂 Folder Structure

project/
│
├── faces/                 # Stored face images
├── attendance.csv         # Attendance log file
├── users.json             # Stores login credentials
├── smart_attendance.py    # Main Python script
└── README.md              # Project documentation


---

## ⚙️ Setup Instructions

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/smart-attendance-system.git
   cd smart-attendance-system
   
2. **Install dependencies:**
   ```bash
   pip install opencv-python pandas fpdf tkcalendar

3. **Run the application:**
   ```bash
   python smart_attendance.py

## 🔐 Default Admin Credentials
Username: admin
Password: password

🔄 To change them, open users.json and update:

{
  "admin": "your_new_password"
}

---

## 🚀 How to Use
Login with admin credentials

Register Face: Enter name & UID (e.g., 24BCS0020) and capture face

Mark Attendance: Recognize faces through webcam and log attendance

View Logs: Search by date or person

Export attendance in Excel or PDF

---

## ✅ UID Format Rule
UID should match the pattern like 24BCS0020 or 23BDM12534

Name should only contain alphabetic characters and spaces

---

## 🛠️ To-Do / Future Features
Add database support (e.g., SQLite, Firebase)

Face recognition using deep learning models (e.g., FaceNet)

Multi-user login with roles (e.g., Admin, Teacher)

Enhanced UI with animations and themes

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📃 License
This project is open-source and available under the MIT License.

---


