import logging
from tkinter import Toplevel, Label, Button, Entry, Frame, messagebox
from tkinter.ttk import Treeview
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
        """Close the database cursor and connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

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
                SELECT u.id, u.fname, u.mname, u.lname, u.username, u.role, a.a_student_id, a.a_status, a.a_date, a.a_approval, a.a_reason
                FROM users u
                LEFT JOIN attendance a ON a.a_student_id = u.id AND DATE(a.a_date) = %s
            """
            self.cursor.execute(query, (today_date,))
            result = self.cursor.fetchall()  # Use fetchall() to handle multiple rows

            if result:
                return result
            else:
                return None
        except Exception as e:
            logging.error(f"Error fetching student data: {e}")
            return None

    def show_instructor_dashboard(self, user_id, username):
        """Show the instructor dashboard."""
        # Fetch instructor data from the database
        instructor_data = self.fetch_instructor_data(username)

        if instructor_data is None:
            messagebox.showerror("Error", "Unable to fetch instructor data.")
            return

        # Create the instructor dashboard window
        instructor_form = Toplevel()
        instructor_form.title(f"Instructor Dashboard - {username}")
        instructor_form.attributes('-fullscreen', True) 

        # Add a Header Navigation
        header_frame = Frame(instructor_form, bg="gray", height=50)
        header_frame.pack(fill="x")  # Fill the entire width of the window

        # Add Menu Buttons in the Header
        Button(header_frame, text="Dashboard", bg="lightblue", command=self.placeholder_action, width=15).pack(side="left", padx=5, pady=10)
        Button(header_frame, text="Profile", bg="lightblue", command=self.placeholder_action, width=15).pack(side="left", padx=5, pady=10)
        Button(header_frame, text="Settings", bg="lightblue", command=self.placeholder_action, width=15).pack(side="left", padx=5, pady=10)
        Button(header_frame, text="Logout", bg="red", fg="white", command=lambda: self.logout(instructor_form), width=15).pack(side="right", padx=5, pady=10)

        # Display welcome message below the header
        Label(instructor_form, text=f"Welcome, Instructor {username}!", font=("Arial", 20)).pack(pady=20)

        # Display instructor details
        Label(instructor_form, text="Instructor Details:", font=("Arial", 14, "bold")).pack(pady=5)
        Label(instructor_form, text=f"User ID: {user_id}", font=("Arial", 12)).pack(pady=5)
        Label(instructor_form, text=f"Full Name: {instructor_data[1]} {instructor_data[2]}", wraplength=800, justify="left", font=("Arial", 12)).pack(pady=10)
        Label(instructor_form, text=f"Username: {instructor_data[4]}", wraplength=800, justify="left", font=("Arial", 12)).pack(pady=5)

        # Fetch daily attendance data for students
        attendance_data = self.fetch_student_daily_attendance()

        if attendance_data is not None:
            # Create the table for displaying attendance
            table_frame = Frame(instructor_form)
            table_frame.pack(pady=20)

            # Create Treeview widget (table)
            tree = Treeview(table_frame, columns=("ID", "First Name", "Middle Name", "Last Name", "Username", "Reason", "Status", "Approval"), show="headings")
            tree.pack(fill="both", expand=True)

            # Define columns
            tree.heading("ID", text="Student ID")
            tree.heading("First Name", text="First Name")
            tree.heading("Middle Name", text="Middle Name")
            tree.heading("Last Name", text="Last Name")
            tree.heading("Username", text="Username")
            tree.heading("Reason", text="Reason")
            tree.heading("Status", text="Status")
            tree.heading("Approval", text="Approval")

            # Add data rows to the table
            for row in attendance_data:
                # Insert the reason in the 6th column (as per Treeview columns defined)
                tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[10], row[7], row[9]))

        else:
            # Display a message within the window if no attendance data is available
            Label(instructor_form, text="No attendance records found for today.", font=("Arial", 14, "italic"), fg="red").pack(pady=30)

    def placeholder_action(self):
        """Placeholder action for future functionality."""
        messagebox.showinfo("Coming Soon", "This feature is under development.")
