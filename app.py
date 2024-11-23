# app.py
from tkinter import *
from tkinter import messagebox
from database import db_instance  # Import the global db_instance from database.py
from instructor_landing import InstructorLanding  # Assuming you have this class defined
from student_landing import StudentLanding  # Assuming you have this class defined
from login import login  # Import the login function

# GUI Setup for Login
app = Tk()
app.title("Login System")
app.geometry("300x200")

# Username Label and Entry
Label(app, text="Username:").pack(pady=5)
username_entry = Entry(app)
username_entry.pack(pady=5)

# Password Label and Entry
Label(app, text="Password:").pack(pady=5)
password_entry = Entry(app, show="*")
password_entry.pack(pady=5)

# Login Button
Button(app, text="Login", command=lambda: login(app, username_entry, password_entry)).pack(pady=10)

# Run the main application loop
app.mainloop()
