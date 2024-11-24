import logging
from tkinter import Toplevel, Frame, Label, Entry, Button, messagebox

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
            check_query = """
                SELECT 1 FROM users WHERE username = %s
            """
            cursor = self.connection.cursor()
            cursor.execute(check_query, (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror("Error", "Username already exists. Please choose another username.")
                cursor.close()
                return False
            
            query = """
                INSERT INTO users (fname, mname, lname, username, password, role) 
                VALUES (%s, %s, %s, %s, %s, 'Student')
            """
            params = (first_name, middle_name, last_name, username, password)

            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            
            return True
        except Exception as e:
            logging.error(f"Error adding student: {e}")
            print(f"Error adding student: {e}")
            return False

    def update_student(self, student_id, first_name, middle_name, last_name, username, password):
        """Update student details in the database."""
        try:
            # Handle the optional middle name by checking if it's empty
            if middle_name:  # If middle name is provided
                query = """
                    UPDATE users
                    SET fname = %s, mname = %s, lname = %s, username = %s, password = %s
                    WHERE id = %s AND role = 'Student'
                """
                params = (first_name, middle_name, last_name, username, password, student_id)
            else:  # If middle name is empty, don't update it
                query = """
                    UPDATE users
                    SET fname = %s, mname = NULL, lname = %s, username = %s, password = %s
                    WHERE id = %s AND role = 'Student'
                """
                params = (first_name, last_name, username, password, student_id)

            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()

            return True
        except Exception as e:
            logging.error(f"Error updating student: {e}")
            print(f"Error updating student: {e}")
            return False

    def delete_student(self, student_id):
        """Delete student from the database."""
        try:
            query = """
                DELETE FROM users WHERE id = %s AND role = 'Student'
            """
            cursor = self.connection.cursor()
            cursor.execute(query, (student_id,))
            self.connection.commit()
            cursor.close()

            return True
        except Exception as e:
            logging.error(f"Error deleting student: {e}")
            print(f"Error deleting student: {e}")
            return False

    def all_students_table(self, parent_frame):
        """Add a table displaying all students in the given parent window."""
        print("Adding all students table...")  # Debugging
        for widget in parent_frame.winfo_children():
            widget.destroy()

        all_students_frame = Frame(parent_frame)
        all_students_frame.pack(pady=30, anchor="w")

        title_label = Label(all_students_frame, text="List of All Students", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=6, pady=10)

        headers = ["ID", "First Name", "Middle Name", "Last Name", "Username", "View", "Update", "Delete"]
        for idx, header in enumerate(headers):
            Label(all_students_frame, text=header, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", width=20).grid(row=1, column=idx)

        for i, student in enumerate(self.all_students_data, start=2):
            for j, value in enumerate(student[:5]):
                Label(all_students_frame, text=value, borderwidth=1, relief="solid", width=20).grid(row=i, column=j)

            view_button = Button(
                all_students_frame,
                text="View",
                bg="blue",
                fg="white",
                command=lambda s=student: self.view_student_details(s),
            )
            view_button.grid(row=i, column=5)

            update_button = Button(
                all_students_frame,
                text="Update",
                bg="orange",
                fg="white",
                command=lambda s=student: self.update_student_form(s, parent_frame),
            )
            update_button.grid(row=i, column=6)

            delete_button = Button(
                all_students_frame,
                text="Delete",
                bg="red",
                fg="white",
                command=lambda s=student: self.delete_student_confirm(s[0], parent_frame),
            )
            delete_button.grid(row=i, column=7)

        add_student_button = Button(
            all_students_frame, text="Add Student", bg="green", fg="white", command=lambda: self.add_student_form(parent_frame)
        )
        add_student_button.grid(row=len(self.all_students_data) + 2, column=0, columnspan=8, pady=20)


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
        """Submit the form to add the student data."""
        first_name = entries["First Name"].get()
        middle_name = entries["Middle Name"].get()
        last_name = entries["Last Name"].get()
        username = entries["Username"].get()
        password = entries["Password"].get()

        print(f"First Name: {first_name}, Last Name: {last_name}, Username: {username}")  

        if not all([first_name, last_name, username, password]):
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        # Call the add_student method
        if self.add_student(first_name, middle_name, last_name, username, password):
            messagebox.showinfo("Success", "Student added successfully.")
            self.fetch_all_students()
            self.all_students_table(add_student_window.master)
            add_student_window.destroy()  # Close the form window
        else:
            messagebox.showerror("Error", "Failed to add student.")


    def update_student_form(self, student, parent_window):
        """Open a form to update student details."""
        student_id, first_name, middle_name, last_name, username = student

        update_window = Toplevel(parent_window)
        update_window.title("Update Student Details")
        update_window.geometry("400x400")

        labels = ["First Name", "Middle Name", "Last Name", "Username", "Password"]
        entries = {}

        for idx, label in enumerate(labels):
            Label(update_window, text=label).grid(row=idx, column=0, padx=10, pady=10, sticky="e")
            entry = Entry(update_window, show="*" if label == "Password" else None)
            entry.grid(row=idx, column=1, padx=10, pady=10)
            entries[label] = entry

        # Pre-fill with the current student data
        entries["First Name"].insert(0, first_name)
        entries["Middle Name"].insert(0, middle_name)  # This will be pre-filled, but can be left blank
        entries["Last Name"].insert(0, last_name)
        entries["Username"].insert(0, username)

        submit_button = Button(update_window, text="Submit", bg="blue", fg="white", 
                            command=lambda: self.submit_update(student_id, entries, update_window))
        submit_button.grid(row=len(labels), column=0, columnspan=2, pady=20)

    def submit_update(self, student_id, entries, update_window):
        """Submit the form to update the student's data."""
        first_name = entries["First Name"].get()
        middle_name = entries["Middle Name"].get()  # This can be empty
        last_name = entries["Last Name"].get()
        username = entries["Username"].get()
        password = entries["Password"].get()

        if not all([first_name, last_name, username, password]):
            messagebox.showerror("Error", "First Name, Last Name, Username, and Password must be filled out.")
            return

        if self.update_student(student_id, first_name, middle_name, last_name, username, password):
            messagebox.showinfo("Success", "Student updated successfully.")
            self.fetch_all_students()
            self.all_students_table(update_window.master)
            update_window.destroy()  # Close the update form window
        else:
            messagebox.showerror("Error", "Failed to update student.")

    def delete_student_confirm(self, student_id, parent_window):
        """Confirm before deleting the student."""
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this student?")
        if response:
            if self.delete_student(student_id):
                messagebox.showinfo("Success", "Student deleted successfully.")
                self.fetch_all_students()
                self.all_students_table(parent_window)
            else:
                messagebox.showerror("Error", "Failed to delete student.")

    def view_student_details(self, student):
        """Show detailed student information."""
        student_id, fname, mname, lname, username = student
        messagebox.showinfo("Student Details", f"ID: {student_id}\nName: {fname} {mname} {lname}\nUsername: {username}")
        
    def show_students(self):
        """Display the list of all students in a new window."""
        print('click')
        
        student_list_window = Toplevel()
        student_list_window.title("Student List")
        
        self.fetch_all_students()
        self.all_students_table(student_list_window)
