# instructor_landing.py
from tkinter import messagebox

class InstructorLanding:
    def __init__(self, connection, main_app):
        """Initialize the InstructorLanding class with a database connection."""
        self.connection = connection
        self.cursor = connection.cursor()
        self.main_app = main_app  # Store the reference to the main login app

    def close(self):
        """Close the database cursor and connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    # other methods...

    def logout(self, instructor_form):
        """Handle the logout functionality."""
        instructor_form.destroy()  # Close the current form
        self.main_app.deiconify()  # Show the main login window again
        messagebox.showinfo("Logged Out", "You have been logged out successfully.")


    def fetch_instructor_data(self, username):
        """Fetch instructor-specific data from the database."""
        try:
            # Ensure the query is correct and the instructor exists in the database
            query = "SELECT * FROM users WHERE username = %s AND role = 'Instructor'"
            self.cursor.execute(query, (username,))
            return self.cursor.fetchone()  # Returns a tuple or None if no match
        except Exception as e:
            print(f"Error fetching instructor data: {e}")
            return None

    def show_instructor_dashboard(self, username):
        """Show the instructor dashboard."""
        # Fetch instructor data from the database
        instructor_data = self.fetch_instructor_data(username)

        if instructor_data is None:
            # Handle case where no data is found for the instructor
            messagebox.showerror("Error", "Unable to fetch instructor data.")
            return

        # Create the instructor dashboard window
        instructor_form = Toplevel()
        instructor_form.title(f"Instructor Dashboard - {username}")
        instructor_form.geometry("400x300")

        # Display welcome message
        Label(instructor_form, text=f"Welcome, Instructor {username}!", font=("Arial", 16)).pack(pady=20)

        # Display the instructor data (adjust to show relevant fields)
        Label(instructor_form, text="Instructor Details:", font=("Arial", 12, "bold")).pack(pady=5)
        # Here, you can choose to display specific fields from the `instructor_data` tuple instead of the whole tuple
        Label(instructor_form, text=f"Full Name: {instructor_data[1]} {instructor_data[2]}", wraplength=350, justify="left").pack(pady=10)
        Label(instructor_form, text=f"Username: {instructor_data[4]}", wraplength=350, justify="left").pack(pady=5)

        # Placeholder for additional features (e.g., buttons for instructor-specific actions)
        Label(instructor_form, text="Actions coming soon!").pack(pady=20)

        # Logout button that closes the current form
        Button(instructor_form, text="Logout", command=instructor_form.destroy).pack(pady=20)
