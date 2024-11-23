# login.py
from student_landing import StudentLanding
from instructor_landing import InstructorLanding  # Import InstructorLanding
from tkinter import messagebox
from database import db_instance  # Import the global db_instance from database.py

def login(app, username_entry, password_entry):
    """Handle the login process."""
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username and password fields are not empty
    if not username or not password:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    # Verify login credentials
    user_info = db_instance.verify_login(username, password)
    if user_info:
        user_id, role = user_info
        messagebox.showinfo("Success", f"Welcome {role} {username}!")

        try:
            # Get database connection
            connection = db_instance.get_db_connection()

            if role == "Instructor":
                # Create InstructorLanding instance and pass user_id, username, and app
                instructor_landing = InstructorLanding(connection, app)
                instructor_landing.show_instructor_dashboard(user_id, username)
                app.withdraw()  # Hide the login window
            elif role == "Student":
                # Create StudentLanding instance and pass user_id, username, and app
                student_landing = StudentLanding(connection, app)
                student_landing.show_student_dashboard(user_id, username)
                app.withdraw()  # Hide the login window
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")
