import logging
from tkinter import Toplevel, Label, Button, Frame, messagebox, Canvas, Scrollbar, Entry
import threading
import time
from datetime import datetime
from list_students import List_students
import pytz

today_date = datetime.now(pytz.timezone('Asia/Manila')).strftime('%Y-%m-%d')

class InstructorLanding:
    def __init__(self, connection, main_app):
        """Initialize the InstructorLanding class with a database connection."""
        self.connection = connection
        self.cursor = connection.cursor()
        self.main_app = main_app
        self.attendance_data = []  
        self.all_students_data = [] 
        self.refresh_interval = 3
        
        # Initialize List_students with the database connection
        self.list_students = List_students(self.connection) 
        
    def logout(self, instructor_form):
        """Handle the logout functionality."""
        try:
            # Close the instructor window (instructor_form)
            instructor_form.destroy()

            # Ensure the main window (main_app) is shown again
            if hasattr(self.main_app, "deiconify"):
                self.main_app.deiconify()  # Show the main window again
                logging.info("Main app window re-shown.")
            else:
                logging.error("Main app window not found or 'deiconify' method unavailable.")
            
            # Display a confirmation message
            messagebox.showinfo("Logged Out", "You have been logged out successfully.")
        except Exception as e:
            logging.error(f"Error during logout: {e}")
            messagebox.showerror("Error", f"Failed to log out: {e}")


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
        """Fetch student-specific data with attendance records for today."""
        try:
            query = """
                SELECT u.id, u.fname, u.mname, u.lname, u.username, a.a_reason, a.a_status, a.a_approval, a.a_date, u.role, a.a_student_id
                FROM users u
                INNER JOIN attendance a ON a.a_student_id = u.id AND DATE(a.a_date) = %s
            """
            self.cursor.execute(query, (today_date,))
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f"Error fetching student data: {e}")
            return None

  
    

   


    def show_students(self, parent=None):
            """Display the list of all students in a new window."""
            print("Fetching students...")
            
            # Fetch all students from List_students instance
            self.list_students.fetch_all_students()  # Call the fetch method of List_students
            
            # Debugging output to confirm students are fetched
            print(f"Fetched students data: {self.list_students.all_students_data}")
            
            # Create a new window to display the students
            student_list_window = Toplevel()
            student_list_window.title("Student List")
            
            # Now call the method to display the students' table
            self.list_students.all_students_table(student_list_window)




   
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
        # instructor_form.attributes('-fullscreen', True)

        # Add header
        self.create_header(instructor_form, lambda: self.logout(instructor_form))

        Label(instructor_form, text=f"Welcome, Instructor {username}!", font=("Arial", 20)).pack(pady=20)

        # Fetch initial daily attendance data for students
        self.attendance_data = self.fetch_student_daily_attendance()

        if self.attendance_data is not None:
            canvas = Canvas(instructor_form)
            canvas.pack(side="top", fill="both", expand=True, padx=20, pady=20)

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

            # Add table header for attendance
            self.add_table_header(scrollable_frame)

            # Display table rows for attendance
            self.display_table_rows(scrollable_frame)

            # Start a thread for real-time updates
            self.polling_thread = threading.Thread(target=self.poll_database, args=(instructor_form, scrollable_frame))
            self.polling_thread.daemon = True  # This ensures the thread will exit when the program exits
            self.polling_thread.start()

        else:
            Label(instructor_form, text="No attendance records found for today.", font=("Arial", 14, "italic"), fg="red").pack(pady=30)

    def create_header(self, parent, logout_action):
        """Create a header navigation bar with menu buttons."""
        header_frame = Frame(parent, bg="gray", height=50)
        header_frame.pack(fill="x")

        # Add Menu Buttons in the Header
        Button(header_frame, text="Dashboard", bg="lightblue", command=self.placeholder_action, width=15).pack(side="left", padx=5, pady=10)
        Button(header_frame, text="Profile", bg="lightblue", command=self.placeholder_action, width=15).pack(side="left", padx=5, pady=10)
        Button(header_frame, text="Settings", bg="lightblue", command=self.placeholder_action, width=15).pack(side="left", padx=5, pady=10)

        # Updated "Students" Button to Show All Students List
        Button(header_frame, text="Students", bg="lightblue", command=lambda: self.show_students(parent), width=15).pack(side="left", padx=5, pady=10)

        Button(header_frame, text="Instructor", bg="lightblue", command=self.placeholder_action, width=15).pack(side="left", padx=5, pady=10)
        Button(header_frame, text="Logout", bg="red", fg="white", command=logout_action, width=15).pack(side="right", padx=5, pady=10)

        return header_frame


    def add_table_header(self, scrollable_frame):
        """Add the header for the attendance table."""
        headers = ["ID", "First Name", "Middle Name", "Last Name", "Username", "Reason", "Status", "Approval", "Date"]
        for idx, header in enumerate(headers):
            Label(scrollable_frame, text=header, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", width=20).grid(row=0, column=idx)

    def display_table_rows(self, scrollable_frame):
        """Display rows of student data in the table."""
        for i, row in enumerate(self.attendance_data, start=1):
            # Display the attendance details
            for j, value in enumerate(row[:9]):  # Exclude unnecessary fields
                Label(scrollable_frame, text=value, borderwidth=1, relief="solid", width=20).grid(row=i, column=j)

            if row[7] == 'Pending': 
                action_frame = Frame(scrollable_frame)
                action_frame.grid(row=i, column=len(self.attendance_data[0]), padx=10, pady=5)

                approve_button = Button(action_frame, text="Approve", bg="green", fg="white",
                                        command=lambda r=row, sf=scrollable_frame: self.update_attendance_status_by_row(r, "Approved", sf))
                approve_button.pack(side="left", padx=5)

                decline_button = Button(action_frame, text="Decline", bg="red", fg="white",
                                        command=lambda r=row, sf=scrollable_frame: self.update_attendance_status_by_row(r, "Declined", sf))
                decline_button.pack(side="left", padx=5)

   

    def update_attendance_status_by_row(self, row, status, scrollable_frame):
        """Update the attendance approval status in the database for a specific row."""
        try:
            student_id = row[0] 
            attendance_date = today_date 

            logging.info(f"Updating attendance status: student_id={student_id}, date={attendance_date}, status={status}")

            query = """
                UPDATE attendance 
                SET a_approval = %s 
                WHERE a_student_id = %s AND DATE(a_date) = %s
            """
            self.cursor.execute(query, (status, student_id, attendance_date))
            self.connection.commit()

            # After updating, refresh the data and UI
            self.refresh_table(scrollable_frame)

        except Exception as e:
            logging.error(f"Error updating attendance status: {e}")
            messagebox.showerror("Error", f"Failed to update attendance status: {e}")

    def refresh_table(self, scrollable_frame):
        """Refresh the table by fetching the latest data from the database and updating the UI."""
        if scrollable_frame.winfo_exists():  # Ensure the frame still exists
            self.attendance_data = self.fetch_student_daily_attendance()

            if self.attendance_data is not None:
                # Clear existing rows in the table
                for widget in scrollable_frame.winfo_children():
                    widget.grid_forget()  # grid_forget() will remove the widget but keep its position

                # Re-add the table header
                self.add_table_header(scrollable_frame)

                # Re-display the table rows with updated data
                self.display_table_rows(scrollable_frame)
            else:
                logging.error("No data fetched during refresh.")
        else:
            logging.error("The scrollable_frame no longer exists.")


    def poll_database(self, instructor_form, scrollable_frame):
        """Poll the database periodically for updates."""
        while True:
            time.sleep(self.refresh_interval)
            
            if scrollable_frame.winfo_exists():  # Ensure the scrollable_frame is still valid
                instructor_form.after(0, self.refresh_table, scrollable_frame)  # Safely update the UI
            else:
                logging.error("scrollable_frame no longer exists. Stopping polling.")
                break  # Stop polling if the scrollable_frame is destroyed


