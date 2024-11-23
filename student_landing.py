from tkinter import Toplevel, Label, Button, messagebox

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

    def fetch_student_data(self, username):
        """Fetch student-specific data from the database."""
        try:
            # Query to fetch student data based on username
            query = "SELECT id, fname, mname, lname, username, role FROM users WHERE username = %s"
            self.cursor.execute(query, (username,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching student data: {e}")
            return None

    def show_student_dashboard(self, username):
        """Display the student dashboard in fullscreen with header navigation and horizontal table format."""
        # Fetch student data
        student_data = self.fetch_student_data(username)

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
        Button(header_frame, text="Dashboard", font=("Arial", 12), command=lambda: self.show_student_dashboard(username)).grid(row=0, column=0, padx=20)
        Button(header_frame, text="Settings", font=("Arial", 12), command=self.show_settings).grid(row=0, column=1, padx=20)
        Button(header_frame, text="Help", font=("Arial", 12), command=self.show_help).grid(row=0, column=2, padx=20)
        Button(header_frame, text="Logout", font=("Arial", 12), command=student_form.destroy).grid(row=0, column=3, padx=20)

        # Welcome label centered in the window
        welcome_label = Label(student_form, text=f"Welcome, {username}!", font=("Arial", 16, "bold"))
        welcome_label.grid(row=1, column=0, columnspan=4, pady=20, sticky="n")

        # Display student data or error message
        if student_data:
            # Extract student details
            id, fname, mname, lname, username, role = student_data
            full_name = f"{fname} {mname if mname else ''} {lname}"

            Label(student_form, text="Student ID", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky="ew")
            Label(student_form, text="Full Name", font=("Arial", 12, "bold")).grid(row=2, column=1, padx=10, pady=5, sticky="ew")
            Label(student_form, text="Actions", font=("Arial", 12, "bold")).grid(row=2, column=2, padx=10, pady=5, sticky="ew")

            # Student data row (centered content)
            Label(student_form, text=f"{id}", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=5, sticky="ew")
            Label(student_form, text=full_name, font=("Arial", 10)).grid(row=3, column=1, padx=10, pady=5, sticky="ew")

            # Create "Absent" and "Present" buttons under the Actions column
            absent_button = Button(student_form, text="Absent", font=("Arial", 10), command=lambda: self.mark_absent(id))
            absent_button.grid(row=3, column=2, padx=5, pady=5, sticky="ew")

            present_button = Button(student_form, text="Present", font=("Arial", 10), command=lambda: self.mark_present(id))
            present_button.grid(row=3, column=3, padx=5, pady=5, sticky="ew")

        else:
            # If no data found or error occurred
            Label(student_form, text="No data found or error occurred.", fg="red", font=("Arial", 12)).grid(row=3, column=0, columnspan=4, pady=10, sticky="n")

        # Placeholder for additional features (centered content)
        Label(student_form, text="Actions coming soon!", font=("Arial", 10)).grid(row=4, column=0, columnspan=4, pady=20, sticky="n")



      

    def show_settings(self):
        """Display settings page (placeholder function)."""
        print("Settings page")

    def show_help(self):
        """Display help page (placeholder function)."""
        print("Help page")
