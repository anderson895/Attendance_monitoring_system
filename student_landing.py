from tkinter import Toplevel, Label, Button, messagebox
import datetime

class StudentLanding:
    def __init__(self, connection):
        """Initialize the StudentLanding class with a database connection."""
        self.connection = connection
        self.cursor = connection.cursor()

    def close(self):
        """Close the database cursor and connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def fetch_student_DailyAttendance(self, user_id):
        """Fetch student-specific data from the database."""
        try:
            # Query to fetch student data based on user_id
            query = """
                        SELECT users.id, users.fname, users.mname, users.lname, users.username, users.role, 
                               attendance.a_student_id, attendance.a_status, attendance.a_date, 
                               CASE 
                                   WHEN attendance.a_student_id IS NULL THEN 'Not Exist'
                                   ELSE 'Exist'
                               END AS attendance_status
                        FROM users
                        LEFT JOIN attendance ON users.id = attendance.a_student_id
                        WHERE users.id = %s;
                    """
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchall()  # Use fetchall() to handle multiple rows

            if result:
                return result
            else:
                # Handle the case where no data is found
                return None
        except Exception as e:
            print(f"Error fetching student data: {e}")
            return None

    def fetch_student_data(self, user_id):
        """Fetch student-specific data from the database."""
        try:
            # Query to fetch student data based on user_id
            query = "SELECT id, fname, mname, lname, username, role FROM users WHERE id = %s"
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching student data: {e}")
            return None

    def show_student_dashboard(self, user_id, username):
        # Fetch student data
        student_data = self.fetch_student_DailyAttendance(user_id)
        
        if student_data is None:
            print("No student data found")
            messagebox.showerror("Error", "Student data not found or error occurred.")
            return

        # Create the student dashboard window
        student_form = Toplevel()
        student_form.title(f"Student Dashboard - {username}")
        student_form.geometry("800x600")  # Set the width and height here

        # Header Navigation Row
        header_frame = Label(student_form, bg="lightblue")
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew", pady=10)

        # Ensure the navigation bar stretches across the full width
        student_form.grid_columnconfigure(0, weight=1)  # Ensure the column is resizable
        student_form.grid_columnconfigure(1, weight=1)
        student_form.grid_columnconfigure(2, weight=1)
        student_form.grid_columnconfigure(3, weight=1)

        # Navigation Buttons in Header
        Button(header_frame, text="Dashboard", font=("Arial", 12), command=lambda: self.show_student_dashboard(user_id, username)).grid(row=0, column=0, padx=20)
        Button(header_frame, text="Settings", font=("Arial", 12), command=self.show_settings).grid(row=0, column=1, padx=20)
        Button(header_frame, text="Help", font=("Arial", 12), command=self.show_help).grid(row=0, column=2, padx=20)
        Button(header_frame, text="Logout", font=("Arial", 12), command=student_form.destroy).grid(row=0, column=3, padx=20)

        # Display student's full name in the welcome label
        full_name = ""
        attendance_status = ""

        # Loop through the results and handle each row
        for row in student_data:
            # Unpack the values from each row
            user_id, fname, mname, lname, username, role, a_student_id, a_status, a_date, attendance_status = row
            full_name = f"{fname} {mname if mname else ''} {lname}"

            # Display the "Daily Attendance" header label
            daily_attendance_label = Label(student_form, text="Daily Attendance", font=("Arial", 14, "bold"))
            daily_attendance_label.grid(row=1, column=0, columnspan=4, pady=20, sticky="n")

            # Display student data or error message
            Label(student_form, text="Student ID", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky="ew")
            Label(student_form, text="Full Name", font=("Arial", 12, "bold")).grid(row=2, column=1, padx=10, pady=5, sticky="ew")
            Label(student_form, text="Attendance Status", font=("Arial", 12, "bold")).grid(row=2, column=2, padx=10, pady=5, sticky="ew")
            Label(student_form, text="Actions", font=("Arial", 12, "bold")).grid(row=2, column=3, padx=10, pady=5, sticky="ew")

            # Student data row (centered content)
            Label(student_form, text=f"{user_id}", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=5, sticky="ew")
            Label(student_form, text=full_name, font=("Arial", 10)).grid(row=3, column=1, padx=10, pady=5, sticky="ew")
            Label(student_form, text=attendance_status, font=("Arial", 10)).grid(row=3, column=2, padx=10, pady=5, sticky="ew")

            # Create "Absent" and "Present" buttons under the Actions column
            absent_button = Button(student_form, text="Absent", font=("Arial", 10), command=lambda: self.mark_absent(user_id))
            absent_button.grid(row=3, column=3, padx=5, pady=5, sticky="ew")

            present_button = Button(student_form, text="Present", font=("Arial", 10), command=lambda: self.mark_present(user_id))
            present_button.grid(row=3, column=4, padx=5, pady=5, sticky="ew")

        if not student_data:
            # If no data found or error occurred
            Label(student_form, text="No attendance record found.", fg="red", font=("Arial", 12)).grid(row=3, column=0, columnspan=4, pady=10, sticky="n")

        # Welcome label centered in the window
        welcome_label = Label(student_form, text=f"Welcome, {full_name}!", font=("Arial", 16, "bold"))
        welcome_label.grid(row=1, column=0, columnspan=4, pady=20, sticky="n")
        
        # Placeholder for additional features (centered content)
        Label(student_form, text="Actions coming soon!", font=("Arial", 10)).grid(row=4, column=0, columnspan=4, pady=20, sticky="n")

    def mark_present(self, student_id):
        """Mark the student as present in the attendance table."""
        try:
            # Get the current date
            current_date = datetime.date.today()

            # Create an INSERT query to mark attendance as 'Present'
            query = """
            INSERT INTO attendance (a_student_id, a_status, a_date) 
            VALUES (%s, %s, %s)
            """
            self.cursor.execute(query, (student_id, 'Present', current_date))
            self.connection.commit()

            # Notify the user that attendance has been marked
            messagebox.showinfo("Success", "Attendance marked as Present.")
        except Exception as e:
            # Handle errors, if any
            messagebox.showerror("Error", f"An error occurred: {e}")

    def mark_absent(self, student_id):
        """Mark the student as absent in the attendance table."""
        try:
            # Get the current date
            current_date = datetime.date.today()

            # Create an INSERT query to mark attendance as 'Absent'
            query = """
            INSERT INTO attendance (a_student_id, a_status, a_date) 
            VALUES (%s, %s, %s)
            """
            self.cursor.execute(query, (student_id, 'Absent', current_date))
            self.connection.commit()

            # Notify the user that attendance has been marked
            messagebox.showinfo("Success", "Attendance marked as Absent.")
        except Exception as e:
            # Handle errors, if any
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_settings(self):
        """Display settings page (placeholder function)."""
        print("Settings page")

    def show_help(self):
        """Display help page (placeholder function)."""
        print("Help page")
