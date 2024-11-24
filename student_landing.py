from tkinter import Toplevel, Label, Button, Entry, messagebox
from datetime import datetime
import pytz

# Correct usage of datetime
today_date = datetime.now(pytz.timezone('Asia/Manila')).strftime('%Y-%m-%d')

class StudentLanding:
    def __init__(self, connection, main_app):
        """Initialize the StudentLanding class with a database connection."""
        self.connection = connection
        self.cursor = connection.cursor()
        self.main_app = main_app 

    def logout(self, student_form):
        """Handle the logout functionality."""
        student_form.destroy()

        # Show the main login window again
        if self.main_app:
            self.main_app.deiconify() 
            self.main_app.lift() 

        # Optionally reset any session variables or states
        print("Logout successful - Login form should now be visible.")

        # Display a message box to confirm logout
        messagebox.showinfo("Logged Out", "You have been logged out successfully.")

    def fetch_student_AttendanceHistory(self, user_id):
        """Fetch all attendance history for the student."""
        try:
            # Query to fetch attendance history
            query = """
                SELECT a.a_date, a.a_status, a.a_reason
                FROM attendance a
                WHERE a.a_student_id = %s
                ORDER BY a.a_date DESC
            """
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchall()  # Fetch all rows for attendance history
        except Exception as e:
            print(f"Error fetching attendance history: {e}")
            return None


    def fetch_student_DailyAttendance(self, user_id):
        """Fetch student-specific data from the database."""
        try:
            # Query to fetch student data based on user_id
            query = """
                SELECT u.id, u.fname, u.mname, u.lname, u.username, u.role, a.a_student_id, a.a_status, a.a_date
                FROM users u
                LEFT JOIN attendance a ON a.a_student_id = u.id AND DATE(a.a_date) = %s
                WHERE u.id = %s
            """
            self.cursor.execute(query, (today_date, user_id))
            result = self.cursor.fetchall()  # Use fetchall() to handle multiple rows

            if result:
                return result
            else:
                return None
        except Exception as e:
            print(f"Error fetching student data: {e}")
            return None

    def fetch_student_data(self, user_id):
        """Fetch student-specific data from the database."""
        try:    
            query = "SELECT id, fname, mname, lname, username, role FROM users WHERE id = %s"
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching student data: {e}")
            return None

    def show_student_dashboard(self, user_id, username):
        student_data = self.fetch_student_DailyAttendance(user_id)
        attendance_history = self.fetch_student_AttendanceHistory(user_id)

        # Create the student dashboard window
        student_form = Toplevel()
        student_form.title(f"Student Dashboard - {username}")
        student_form.geometry("900x600")

        # Set the background color and title font
        student_form.config(bg="#f5f5f5")

        # Header Section with a clearer background and navigation options
        header_frame = Label(student_form, bg="#0078D4", height=3)
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=10)

        # Ensure the grid expands to fill the entire window width
        student_form.grid_columnconfigure(0, weight=1)
        student_form.grid_columnconfigure(1, weight=1)
        student_form.grid_columnconfigure(2, weight=1)
        student_form.grid_columnconfigure(3, weight=1)

       
        # Display student's full name in the welcome label
        full_name = ""
        student_info = self.fetch_student_data(user_id)

 


        if student_info:
            user_id, fname, mname, lname, username, role = student_info
            full_name = f"{fname} {mname if mname else ''} {lname}"

            # Add Buttons in the header with clear distinctions
        Button(header_frame, text=f"{full_name}", font=("Arial", 12), bg="#005A9E", fg="white", relief="flat").grid(row=0, column=0, padx=20)
        Button(header_frame, text="Logout", font=("Arial", 12), command=lambda: self.logout(student_form), bg="#E57373", fg="white", relief="flat").grid(row=0, column=3, padx=20)

        # Display "Daily Attendance" header label (Center it)
        daily_attendance_label = Label(student_form, text="Daily Attendance", font=("Arial", 16, "bold"), bg="#f5f5f5")
        daily_attendance_label.grid(row=1, column=0, columnspan=4, pady=20, sticky="nsew")


    
        # Add Attendance buttons below Student ID and Full Name
        attendance_status = "Not Exist"
        if student_data:
            for row in student_data:
                user_id, fname, mname, lname, username, role, a_student_id, a_status, a_date = row
                if a_status:
                    attendance_status = 'Exist'

        if attendance_status == 'Exist':
            absent_button = Button(student_form, text="Absent", font=("Arial", 10), state="disabled", relief="flat", bg="#E0E0E0", width=4)
            absent_button.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
            present_button = Button(student_form, text="Present", font=("Arial", 10), state="disabled", relief="flat", bg="#E0E0E0", width=4)
            present_button.grid(row=4, column=2, padx=5, pady=5, sticky="ew")
        else:
            absent_button = Button(student_form, text="Absent", font=("Arial", 10), command=lambda: self.ask_for_absence_reason(user_id, username, student_form), relief="flat", bg="#FF7043", fg="white", width=4)
            absent_button.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
            present_button = Button(student_form, text="Present", font=("Arial", 10), command=lambda: self.mark_present(user_id, username, student_form), relief="flat", bg="#66BB6A", fg="white", width=4)
            present_button.grid(row=4, column=2, padx=5, pady=5, sticky="ew")

       # Display attendance history with enhanced design
        history_label = Label(student_form, text="Attendance History", font=("Arial", 14, "bold"), bg="#f5f5f5")
        history_label.grid(row=5, column=0, columnspan=4, pady=20)

        if attendance_history:
            for index, (a_date, a_status, a_reason) in enumerate(attendance_history, start=6):
                # Determine the foreground color based on attendance status
                color = "#FF0000" if a_status.lower() == "absent" else "#008000"  # Red for Absent, Green for Present
                status_display = f"{a_status} - {a_reason if a_reason else 'N/A'}"

                Label(
                    student_form,
                    text=f"{a_date}: {status_display}",
                    font=("Arial", 10),
                    bg="#f5f5f5",
                    fg=color  # Set color dynamically
                ).grid(row=index, column=0, columnspan=4, padx=10, pady=5)
        else:
            Label(
                student_form,
                text="No attendance history found.",
                font=("Arial", 10),
                bg="#f5f5f5"
            ).grid(row=6, column=0, columnspan=4, padx=10, pady=5)




    def ask_for_absence_reason(self, student_id, username, student_form):
        """Ask the student for a reason if marking as absent."""
        # Create a new top-level window to input the reason for absence
        reason_form = Toplevel(student_form)
        reason_form.title("Enter Absence Reason")
        reason_form.geometry("400x200")

        # Add label and entry for the reason
        Label(reason_form, text="Please provide a reason for your absence:", font=("Arial", 12)).pack(pady=10)
        reason_entry = Entry(reason_form, font=("Arial", 12), width=30)
        reason_entry.pack(pady=10)

        # Add submit button
        Button(reason_form, text="Submit", font=("Arial", 12), command=lambda: self.mark_absent_with_reason(student_id, username, reason_entry.get(), reason_form, student_form)).pack(pady=10)

    def mark_absent_with_reason(self, student_id, username, reason, reason_form, student_form):
        """Mark the student as absent with a reason."""
        if not reason:
            messagebox.showwarning("Input Error", "Please provide a reason for your absence.")
            return

        try:
            query = """
            INSERT INTO attendance (a_student_id, a_status, a_date, a_reason) 
            VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (student_id, 'Absent', today_date, reason))
            self.connection.commit()

            messagebox.showinfo("Success", "Attendance marked as Absent.")
            reason_form.destroy()
            student_form.destroy()
            self.show_student_dashboard(student_id, username)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def mark_present(self, student_id, username, student_form):
        """Mark the student as present in the attendance table."""
        try:
            query = """
            INSERT INTO attendance (a_student_id, a_status, a_date) 
            VALUES (%s, %s, %s)
            """
            self.cursor.execute(query, (student_id, 'Present', today_date))
            self.connection.commit()

            messagebox.showinfo("Success", "Attendance marked as Present.")
            student_form.destroy()
            self.show_student_dashboard(student_id, username)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_settings(self):
        """Display settings page (placeholder function)."""
        print("Settings page")

    def show_help(self):
        """Display help page (placeholder function)."""
        print("Help page")
