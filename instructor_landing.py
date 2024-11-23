from tkinter import Toplevel, Label, Button, messagebox

class InstructorLanding:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def fetch_instructor_data(self, username):
        """Fetch instructor-specific data from the database."""
        try:
            query = "SELECT * FROM users WHERE username = %s AND role = 'Instructor'"
            self.cursor.execute(query, (username,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching instructor data: {e}")
            return None

    def show_instructor_dashboard(self, username):
        """Show the instructor dashboard."""
        instructor_data = self.fetch_instructor_data(username)

        if instructor_data is None:
            messagebox.showerror("Error", "Unable to fetch instructor data.")
            return

        instructor_form = Toplevel()
        instructor_form.title("Instructor Dashboard")
        instructor_form.geometry("400x300")

        Label(instructor_form, text=f"Welcome, Instructor {username}!", font=("Arial", 16)).pack(pady=20)
        
        # Display fetched data
        Label(instructor_form, text="Instructor Details:", font=("Arial", 12, "bold")).pack(pady=5)
        Label(instructor_form, text=f"{instructor_data}", wraplength=350, justify="left").pack(pady=10)

        # Placeholder for additional features
        Label(instructor_form, text="Actions coming soon!").pack(pady=20)

        # Logout button
        Button(instructor_form, text="Logout", command=instructor_form.destroy).pack(pady=20)
