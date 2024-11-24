import logging
from tkinter import Toplevel, Frame, Label, Entry, Button, messagebox

# list_students.py
class List_students:
    def __init__(self, connection):
        self.connection = connection
        self.all_students_data = []

    def fetch_all_students(self):
        """Fetch all students from the database."""
        if not self.connection:
            print("Error: No valid database connection.")
            return None

        try:
            query = """
                SELECT id, fname, mname, lname, username FROM users WHERE role = 'Student'
            """
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            print(f"Fetched students: {result}")  # Debugging print statement

            if result:
                self.all_students_data = result
            else:
                print("No students found in the database.")

            return result
        except Exception as e:
            logging.error(f"Error fetching all students: {e}")
            print(f"Error fetching all students: {e}")
            return None





    def add_student(self, first_name, middle_name, last_name, username, password):
        """Add a new student to the database."""
        try:
            # Check if the username already exists
            check_query = """
                SELECT 1 FROM users WHERE username = %s
            """
            cursor = self.connection.cursor()
            cursor.execute(check_query, (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                # If username exists, show an alert and return False
                messagebox.showerror("Error", "Username already exists. Please choose another username.")
                cursor.close()
                return False
            
            # Insert new student if username does not exist
            query = """
                INSERT INTO users (fname, mname, lname, username, password, role) 
                VALUES (%s, %s, %s, %s, %s, 'Student')
            """
            params = (first_name, middle_name, last_name, username, password)

            cursor.execute(query, params)  # Insert new student
            self.connection.commit()  # Commit the transaction to save the changes

            print("Student added successfully!")  # Debugging
            cursor.close()
            
            # Return True to indicate success
            return True

        except Exception as e:
            logging.error(f"Error adding student: {e}")
            print(f"Error adding student: {e}")
            return False


    def all_students_table(self, parent_frame):
        """Add a table displaying all students in the given parent window."""
        print("Adding all students table...")  # Debugging
        # Clear the frame before repopulating
        for widget in parent_frame.winfo_children():
            widget.destroy()

        # Frame for the table
        all_students_frame = Frame(parent_frame)
        all_students_frame.pack(pady=30, anchor="w")

        # Title for the All Students table
        title_label = Label(all_students_frame, text="List of All Students", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=6, pady=10)

        # Table header
        headers = ["ID", "First Name", "Middle Name", "Last Name", "Username", "View"]
        for idx, header in enumerate(headers):
            Label(all_students_frame, text=header, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", width=20).grid(row=1, column=idx)

        # Populate rows with fetched student data
        for i, student in enumerate(self.all_students_data, start=2):
            print(f"Adding student {i}: {student}")  # Debugging
            for j, value in enumerate(student[:5]):
                Label(all_students_frame, text=value, borderwidth=1, relief="solid", width=20).grid(row=i, column=j)

            # Add "View" button to view student details
            view_button = Button(
                all_students_frame,
                text="View",
                bg="blue",
                fg="white",
                command=lambda s=student: self.view_student_details(s),
            )
            view_button.grid(row=i, column=5)

        # "Add Student" button below the table
        add_student_button = Button(
            all_students_frame, text="Add Student", bg="green", fg="white", command=lambda: self.add_student_form(parent_frame)
        )
        add_student_button.grid(row=len(self.all_students_data) + 2, column=0, columnspan=6, pady=20)



    def add_student_form(self, parent_window):
        """Open a form to add a new student."""
        add_student_window = Toplevel(parent_window)  # Use the passed parent_window as the master
        add_student_window.title("Add New Student")
        add_student_window.geometry("400x400")

        # Labels and input fields
        labels = ["First Name", "Middle Name", "Last Name", "Username", "Password"]
        entries = {}

        for idx, label in enumerate(labels):
            Label(add_student_window, text=label).grid(row=idx, column=0, padx=10, pady=10, sticky="e")
            entry = Entry(add_student_window, show="*" if label == "Password" else None)
            entry.grid(row=idx, column=1, padx=10, pady=10)
            entries[label] = entry

        # Submit button
        submit_button = Button(add_student_window, text="Submit", bg="blue", fg="white", 
                            command=lambda: self.submit_student(entries, add_student_window))
        submit_button.grid(row=len(labels), column=0, columnspan=2, pady=20)



    def submit_student(self, entries, add_student_window):
        """Submit the form and add a new student."""
        first_name = entries["First Name"].get()
        middle_name = entries["Middle Name"].get()
        last_name = entries["Last Name"].get()
        username = entries["Username"].get()
        password = entries["Password"].get()

        if not all([first_name, middle_name, last_name, username, password]):
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        if self.add_student(first_name, middle_name, last_name, username, password):
            # If student added successfully, reload the student list and refresh the table
            self.fetch_all_students()  # Fetch updated list of students
            print("Refreshing student table...")
            self.all_students_table(add_student_window.master)  # Refresh the student list table

            messagebox.showinfo("Success", "Student added successfully.")
            add_student_window.destroy()  # Close only the add student form window
        else:
            messagebox.showerror("Error", "Failed to add student.")





    def view_student_details(self, student):
        """Show detailed student information."""
        student_id, fname, mname, lname, username = student
        messagebox.showinfo("Student Details", f"ID: {student_id}\nName: {fname} {mname} {lname}\nUsername: {username}")
        
    def show_students(self):
        """Display the list of all students in a new window."""
        print('click')
        
        # Create the new window for displaying students
        student_list_window = Toplevel()
        student_list_window.title("Student List")
        
        # First, fetch all students
        self.fetch_all_students()
        
        # Then display the table with the fetched data
        self.all_students_table(student_list_window)


