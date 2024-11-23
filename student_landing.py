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
            query = "SELECT * FROM students WHERE username = %s"
            self.cursor.execute(query, (username,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching student data: {e}")
            return None

    def show_student_dashboard(self, username):
        """Display the student dashboard."""
        # Fetch student data
        student_data = self.fetch_student_data(username)

        # Create the student dashboard window
        student_form = Toplevel()
        student_form.title(f"Student Dashboard - {username}")
        student_form.geometry("400x300")

        # Welcome label
        Label(student_form, text=f"Welcome, Student {username}!", font=("Arial", 16)).pack(pady=20)

        # Display student data or error message
        if student_data:
            Label(student_form, text="Student Details:", font=("Arial", 12, "bold")).pack(pady=5)
            Label(student_form, text=f"{student_data}", wraplength=350, justify="left").pack(pady=10)
        else:
            Label(student_form, text="No data found or error occurred.", fg="red").pack(pady=10)

        # Placeholder for additional features
        Label(student_form, text="Actions coming soon!", font=("Arial", 10)).pack(pady=10)

        # Logout button
        Button(student_form, text="Logout", command=student_form.destroy).pack(pady=20)
