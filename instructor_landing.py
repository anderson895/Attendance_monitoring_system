import logging
from tkinter import Toplevel, Label, Button, Frame, messagebox, Canvas, Scrollbar
from datetime import datetime
import pytz

# Correct usage of datetime
today_date = datetime.now(pytz.timezone('Asia/Manila')).strftime('%Y-%m-%d')

class InstructorLanding:
    def __init__(self, connection, main_app):
        """Initialize the InstructorLanding class with a database connection."""
        self.connection = connection
        self.cursor = connection.cursor()
        self.main_app = main_app

    def close(self):
        """Safely close the database cursor and connection."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except Exception as e:
            logging.error(f"Error while closing resources: {e}")

    def logout(self, instructor_form):
        """Handle the logout functionality."""
        instructor_form.destroy()  # Close the dashboard
        self.main_app.deiconify()  # Show the login window
        messagebox.showinfo("Logged Out", "You have been logged out successfully.")

    def fetch_instructor_data(self, username):
        """Fetch instructor-specific data from the database."""
        try:
            query = "SELECT * FROM users WHERE username = %s AND role = 'Instructor'"
            self.cursor.execute(query, (username,))
            return self.cursor.fetchone()  # Returns a tuple or None if no match
        except Exception as e:
            logging.error(f"Error fetching instructor data: {e}")
            return None

    def fetch_student_daily_attendance(self):
        """Fetch student-specific data from the database."""
        try:
            query = """
                SELECT u.id, u.fname, u.mname, u.lname, u.username,a.a_reason,a.a_status, a.a_approval,  a.a_date, u.role, a.a_student_id
                FROM users u
                LEFT JOIN attendance a ON a.a_student_id = u.id AND DATE(a.a_date) = %s
            """
            self.cursor.execute(query, (today_date,))
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f"Error fetching student data: {e}")
            return None

    def create_header(self, parent, logout_action):
        """Create a header navigation bar with menu buttons."""
        header_frame = Frame(parent, bg="gray", height=50)
        header_frame.pack(fill="x")

        # Add Menu Buttons in the Header
        Button(header_frame, text="Dashboard", bg="lightblue", command=self.placeholder_action, width=15).pack(side="left", padx=5, pady=10)
        Button(header_frame, text="Profile", bg="lightblue", command=self.placeholder_action, width=15).pack(side="left", padx=5, pady=10)
        Button(header_frame, text="Settings", bg="lightblue", command=self.placeholder_action, width=15).pack(side="left", padx=5, pady=10)
        Button(header_frame, text="Logout", bg="red", fg="white", command=logout_action, width=15).pack(side="right", padx=5, pady=10)

        return header_frame

    def placeholder_action(self):
        """Placeholder action for future functionality."""
        messagebox.showinfo("Coming Soon", "This feature is under development.")

    def show_instructor_dashboard(self, user_id, username):
        """Show the instructor dashboard with Approve/Decline buttons per student."""
        instructor_data = self.fetch_instructor_data(username)

        if instructor_data is None:
            messagebox.showerror("Error", "Unable to fetch instructor data.")
            return

        instructor_form = Toplevel()
        instructor_form.title(f"Instructor Dashboard - {username}")
        instructor_form.attributes('-fullscreen', True)

        # Add header
        self.create_header(instructor_form, lambda: self.logout(instructor_form))

        Label(instructor_form, text=f"Welcome, Instructor {username}!", font=("Arial", 20)).pack(pady=20)

        # Fetch daily attendance data for students
        attendance_data = self.fetch_student_daily_attendance()

        if attendance_data is not None:
            # Create a scrollable canvas
            canvas = Canvas(instructor_form)
            canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)

            scrollbar = Scrollbar(instructor_form, orient="vertical", command=canvas.yview)
            scrollbar.pack(side="right", fill="y")

            canvas.configure(yscrollcommand=scrollbar.set)
            scrollable_frame = Frame(canvas)
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

            # Update scroll region dynamically
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            # Create table headers with proper column alignment
            headers = ["ID", "First Name", "Middle Name", "Last Name", "Username", "Reason", "Status", "Approval"]
            for idx, header in enumerate(headers):
                Label(scrollable_frame, text=header, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", width=20).grid(row=0, column=idx)

            # Add header for Action buttons
            Label(scrollable_frame, text="Action", font=("Arial", 10, "bold"), borderwidth=1, relief="solid", width=20).grid(row=0, column=len(headers))

            # Populate rows with data
            for i, row in enumerate(attendance_data, start=1):
                for j, value in enumerate(row[:9]):  # Exclude unnecessary fields
                    Label(scrollable_frame, text=value, borderwidth=1, relief="solid", width=20).grid(row=i, column=j)

                # Add Approve and Decline buttons with proper alignment
                action_frame = Frame(scrollable_frame)
                action_frame.grid(row=i, column=len(headers), padx=10, pady=5)

                approve_button = Button(action_frame, text="Approve", bg="green", fg="white",
                                       command=lambda r=row: self.update_attendance_status_by_row(r, "Approved"))
                approve_button.pack(side="left", padx=5)

                decline_button = Button(action_frame, text="Decline", bg="red", fg="white",
                                        command=lambda r=row: self.update_attendance_status_by_row(r, "Declined"))
                decline_button.pack(side="left", padx=5)

        else:
            Label(instructor_form, text="No attendance records found for today.", font=("Arial", 14, "italic"), fg="red").pack(pady=30)

    def update_attendance_status_by_row(self, row, status):
        """Update the attendance approval status in the database for a specific row."""
        try:
            student_id = row[0]  # Assuming 'Student ID' is in the first column
            attendance_date = today_date  # Use today's date for the attendance update

            # Update the database
            query = """
                UPDATE attendance 
                SET a_approval = %s 
                WHERE a_student_id = %s AND DATE(a_date) = %s
            """
            self.cursor.execute(query, (status, student_id, attendance_date))
            self.connection.commit()

            messagebox.showinfo("Success", f"Attendance status for {row[1]} updated to '{status}'.")
        except Exception as e:
            logging.error(f"Error updating attendance status: {e}")
            messagebox.showerror("Error", "Failed to update attendance status.")
