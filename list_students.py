import logging
from tkinter import Toplevel, Frame, Label, Entry, Button, messagebox
from tkinter import ttk  # Import for ComboBox

class List_users:
    def __init__(self, connection):
        self.connection = connection
        self.all_users_data = []

    def fetch_all_users(self):
        """Fetch all users (students and instructors) from the database."""
        if not self.connection:
            print("Error: No valid database connection.")
            return None

        try:
            query = """
                SELECT id, fname, mname, lname, username, role FROM users
            """
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()

            if result:
                self.all_users_data = result
                return result
            else:
                print("No users found in the database.")
                return []

        except Exception as e:
            logging.error(f"Error fetching all users: {e}")
            print(f"Error fetching all users: {e}")
            return []


    def add_user(self, first_name, middle_name, last_name, username, password, role):
        """Add a new user (Student or Instructor) to the database."""
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
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (first_name, middle_name, last_name, username, password, role)

            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            
            return True
        except Exception as e:
            logging.error(f"Error adding user: {e}")
            print(f"Error adding user: {e}")
            return False

    def update_user(self, user_id, first_name, middle_name, last_name, username, password, role):
        """Update user details in the database."""
        try:
            # Handle the optional middle name by checking if it's empty
            if middle_name:  # If middle name is provided
                query = """
                    UPDATE users
                    SET fname = %s, mname = %s, lname = %s, username = %s, password = %s, role = %s
                    WHERE id = %s
                """
                params = (first_name, middle_name, last_name, username, password, role, user_id)
            else:  # If middle name is empty, don't update it
                query = """
                    UPDATE users
                    SET fname = %s, mname = NULL, lname = %s, username = %s, password = %s, role = %s
                    WHERE id = %s
                """
                params = (first_name, last_name, username, password, role, user_id)

            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()

            return True
        except Exception as e:
            logging.error(f"Error updating user: {e}")
            print(f"Error updating user: {e}")
            return False

    def delete_user(self, user_id):
        """Delete user from the database."""
        try:
            query = """
                DELETE FROM users WHERE id = %s
            """
            cursor = self.connection.cursor()
            cursor.execute(query, (user_id,))
            self.connection.commit()
            cursor.close()

            return True
        except Exception as e:
            logging.error(f"Error deleting user: {e}")
            print(f"Error deleting user: {e}")
            return False

    def all_users_table(self, parent_frame):
        """Add a table displaying all users in the given parent window."""
        print("Adding all users table...")  # Debugging
        for widget in parent_frame.winfo_children():
            widget.destroy()

        all_users_frame = Frame(parent_frame)
        all_users_frame.pack(pady=30, anchor="w")

        title_label = Label(all_users_frame, text="List of All Users (Students and Instructors)", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=9, pady=10)

        headers = ["ID", "First Name", "Middle Name", "Last Name", "Username", "Role", "View", "Update", "Delete"]
        for idx, header in enumerate(headers):
            Label(all_users_frame, text=header, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", width=20).grid(row=1, column=idx)

        for i, user in enumerate(self.all_users_data, start=2):
            for j, value in enumerate(user[:5]):
                Label(all_users_frame, text=value, borderwidth=1, relief="solid", width=20).grid(row=i, column=j)

            role = user[5]  # Assuming the role column is part of the fetched data
            Label(all_users_frame, text=role, borderwidth=1, relief="solid", width=20).grid(row=i, column=5)

            view_button = Button(
                all_users_frame,
                text="View",
                bg="blue",
                fg="white",
                command=lambda u=user: self.view_user_details(u),
            )
            view_button.grid(row=i, column=6)

            update_button = Button(
                all_users_frame,
                text="Update",
                bg="orange",
                fg="white",
                command=lambda u=user: self.update_user_form(u, parent_frame),
            )
            update_button.grid(row=i, column=7)

            delete_button = Button(
                all_users_frame,
                text="Delete",
                bg="red",
                fg="white",
                command=lambda u=user: self.delete_user_confirm(u[0], parent_frame),
            )
            delete_button.grid(row=i, column=8)

        add_user_button = Button(
            all_users_frame, text="Add User", bg="green", fg="white", command=lambda: self.add_user_form(parent_frame)
        )
        add_user_button.grid(row=len(self.all_users_data) + 2, column=0, columnspan=9, pady=20)

    def add_user_form(self, parent_window):
        """Open a form to add a new user (Student or Instructor)."""
        add_user_window = Toplevel(parent_window)  # Use the passed parent_window as the master
        add_user_window.title("Add New User")
        add_user_window.geometry("400x450")

        # Labels and input fields
        labels = ["First Name", "Middle Name", "Last Name", "Username", "Password", "Role"]
        entries = {}

        for idx, label in enumerate(labels[:-1]):  # Exclude Role from labels that need text entry
            Label(add_user_window, text=label).grid(row=idx, column=0, padx=10, pady=10, sticky="e")
            entry = Entry(add_user_window, show="*" if label == "Password" else None)
            entry.grid(row=idx, column=1, padx=10, pady=10)
            entries[label] = entry

        # Role dropdown (ComboBox)
        role_label = Label(add_user_window, text="Role")
        role_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        role_combobox = ttk.Combobox(add_user_window, values=["Student", "Instructor"])
        role_combobox.grid(row=5, column=1, padx=10, pady=10)
        role_combobox.set("Student")  # Default to "Student"
        entries["Role"] = role_combobox

        # Submit button
        submit_button = Button(add_user_window, text="Submit", bg="blue", fg="white", 
                               command=lambda: self.submit_user(entries, add_user_window))
        submit_button.grid(row=6, column=0, columnspan=2, pady=20)

    def submit_user(self, entries, add_user_window):
        """Submit the form to add the user data (Student or Instructor)."""
        first_name = entries["First Name"].get()
        middle_name = entries["Middle Name"].get()
        last_name = entries["Last Name"].get()
        username = entries["Username"].get()
        password = entries["Password"].get()
        role = entries["Role"].get()

        if not all([first_name, last_name, username, password]):
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        # Call the add_user method, passing the role as a parameter
        if self.add_user(first_name, middle_name, last_name, username, password, role):
            messagebox.showinfo("Success", "User added successfully.")
            self.fetch_all_users()
            self.all_users_table(add_user_window.master)
            add_user_window.destroy()  # Close the form window
        else:
            messagebox.showerror("Error", "Failed to add user.")

    def update_user_form(self, user, parent_window):
        """Open a form to update user details (Student or Instructor)."""
        user_id, first_name, middle_name, last_name, username, role = user

        # Create the update window
        update_window = Toplevel(parent_window)
        update_window.title("Update User Details")
        update_window.geometry("400x450")

        # List of labels and dictionary for storing entry fields
        labels = ["First Name", "Middle Name", "Last Name", "Username", "Password", "Role"]
        entries = {}

        # Create entry fields for first name, middle name, last name, username, and password
        for idx, label in enumerate(labels[:-1]):  # Exclude Role from labels that need text entry
            Label(update_window, text=label).grid(row=idx, column=0, padx=10, pady=10, sticky="e")
            entry = Entry(update_window, show="*" if label == "Password" else None)
            entry.grid(row=idx, column=1, padx=10, pady=10)

            # Set default values for the entry fields
            if label == "First Name":
                entry.insert(0, first_name)
            elif label == "Middle Name":
                entry.insert(0, middle_name if middle_name else "")  # Handle None for middle name
            elif label == "Last Name":
                entry.insert(0, last_name)
            elif label == "Username":
                entry.insert(0, username)
            
            entries[label] = entry

        # Role dropdown (ComboBox)
        role_label = Label(update_window, text="Role")
        role_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        role_combobox = ttk.Combobox(update_window, values=["Student", "Instructor"])
        role_combobox.grid(row=5, column=1, padx=10, pady=10)

        # Set default value for role combobox
        role_combobox.set(role)  # Pre-set the current role
        entries["Role"] = role_combobox

        # Submit button
        submit_button = Button(update_window, text="Submit", bg="blue", fg="white", 
                            command=lambda: self.submit_update(user_id, entries, update_window))
        submit_button.grid(row=6, column=0, columnspan=2, pady=20)


    def submit_update(self, user_id, entries, update_window):
        """Submit the form to update the user's data."""
        first_name = entries["First Name"].get()
        middle_name = entries["Middle Name"].get()  # This can be empty
        last_name = entries["Last Name"].get()
        username = entries["Username"].get()
        password = entries["Password"].get()
        role = entries["Role"].get()

        if not all([first_name, last_name, username, password]):
            messagebox.showerror("Error", "First Name, Last Name, Username, and Password must be filled out.")
            return

        if self.update_user(user_id, first_name, middle_name, last_name, username, password, role):
            messagebox.showinfo("Success", "User updated successfully.")
            self.fetch_all_users()
            self.all_users_table(update_window.master)
            update_window.destroy()  # Close the update form window
        else:
            messagebox.showerror("Error", "Failed to update user.")

    def delete_user_confirm(self, user_id, parent_window):
        """Confirm before deleting the user."""
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this user?")
        if response:
            if self.delete_user(user_id):
                messagebox.showinfo("Success", "User deleted successfully.")
                self.fetch_all_users()
                self.all_users_table(parent_window)
            else:
                messagebox.showerror("Error", "Failed to delete user.")

    def view_user_details(self, user):
        """Show detailed user information."""
        user_id, fname, mname, lname, username, role = user
        messagebox.showinfo("User Details", f"ID: {user_id}\nName: {fname} {mname} {lname}\nUsername: {username}\nRole: {role}")
        
    def show_users(self):
        """Display the list of all users in a new window."""
        print('click')
        
        user_list_window = Toplevel()
        user_list_window.title("User List")
        
        self.fetch_all_users()
        self.all_users_table(user_list_window)
