from tkinter import *
from tkinter import messagebox
from database import Database
from instructor_landing import InstructorLanding
from student_landing import StudentLanding

# Create an instance of the Database class
db_instance = Database()

def login():
    username = username_entry.get()
    password = password_entry.get()
    
    if not username or not password:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return
    
    # Verify login credentials
    user_info = db_instance.verify_login(username, password)
    if user_info:
        user_id, role = user_info
        messagebox.showinfo("Success", f"Welcome {role} {username}!")
        
        try:
            connection = db_instance.get_db_connection()
            if role == "Instructor":
                # Create InstructorLanding instance and pass user_id, username
                instructor_landing = InstructorLanding(connection)
                instructor_landing.show_instructor_dashboard(user_id, username)
                app.withdraw()  # Hide the login window
            elif role == "Student":
                # Create StudentLanding instance and pass user_id, username
                student_landing = StudentLanding(connection)
                student_landing.show_student_dashboard(user_id, username)
                app.withdraw()  # Hide the login window
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

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
Button(app, text="Login", command=login).pack(pady=10)

# Run the main application loop
app.mainloop()
