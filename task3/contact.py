import tkinter as tk
from tkinter import messagebox
import mysql.connector

# MySQL Contact Management Class
class ContactManager:
    def __init__(self):
        # Connect to the MySQL database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Use your MySQL username
            password="",  # Use your MySQL password
            database="contactmanagement"
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    # Create the contacts table if it doesn't exist
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                phone VARCHAR(20),
                email VARCHAR(255)
            )
        """)
        self.conn.commit()

    # Add a new contact to the database
    def add_contact(self, name, phone, email):
        self.cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s)", (name, phone, email))
        self.conn.commit()

    # Edit an existing contact in the database
    def edit_contact(self, contact_id, name, phone, email):
        self.cursor.execute("UPDATE contacts SET name=%s, phone=%s, email=%s WHERE id=%s", (name, phone, email, contact_id))
        self.conn.commit()

    # Delete a contact from the database
    def delete_contact(self, contact_id):
        self.cursor.execute("DELETE FROM contacts WHERE id=%s", (contact_id,))
        self.conn.commit()

    # Get all contacts from the database
    def get_contacts(self):
        self.cursor.execute("SELECT * FROM contacts")
        return self.cursor.fetchall()

# GUI for Contact Management System
class ContactApp:
    def __init__(self, root):
        self.manager = ContactManager()
        self.root = root
        self.root.title("Contact Management System")
        self.root.geometry("500x450")
        self.root.configure(bg="#1a1a2e")  # Dark background
        
        # Title Label
        self.title_label = tk.Label(root, text="Contact Management System", font=("Arial", 16, "bold"), bg="#1a1a2e", fg="#00e676")
        self.title_label.pack(pady=10)
        
        # Contact list
        self.contact_listbox = tk.Listbox(root, height=10, width=50, font=("Arial", 12), bg="#252547", fg="white", selectbackground="#007acc", selectforeground="white")
        self.contact_listbox.pack(pady=10)
        self.load_contact_listbox()

        # Buttons for Add, Edit, Delete with new design
        self.button_frame = tk.Frame(root, bg="#1a1a2e")
        self.button_frame.pack(pady=10)

        self.btn_add = tk.Button(self.button_frame, text="Add Contact", font=("Arial", 12), bg="#007acc", fg="white", width=15, command=self.add_contact)
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_edit = tk.Button(self.button_frame, text="Edit Contact", font=("Arial", 12), bg="#007acc", fg="white", width=15, command=self.edit_contact)
        self.btn_edit.grid(row=0, column=1, padx=5)

        self.btn_delete = tk.Button(self.button_frame, text="Delete Contact", font=("Arial", 12), bg="#007acc", fg="white", width=15, command=self.delete_contact)
        self.btn_delete.grid(row=0, column=2, padx=5)

    # Load contacts in the Listbox
    def load_contact_listbox(self):
        self.contact_listbox.delete(0, tk.END)
        contacts = self.manager.get_contacts()
        for contact in contacts:
            self.contact_listbox.insert(tk.END, f"{contact[0]}. {contact[1]} - {contact[2]} - {contact[3]}")

    # Add new contact
    def add_contact(self):
        contact_window = tk.Toplevel(self.root)
        contact_window.title("Add New Contact")
        contact_window.configure(bg="#1a1a2e")

        tk.Label(contact_window, text="Name:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(pady=5)
        entry_name = tk.Entry(contact_window, font=("Arial", 12), width=30, bg="#252547", fg="white")
        entry_name.pack(pady=5)

        tk.Label(contact_window, text="Phone:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(pady=5)
        entry_phone = tk.Entry(contact_window, font=("Arial", 12), width=30, bg="#252547", fg="white")
        entry_phone.pack(pady=5)

        tk.Label(contact_window, text="Email:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(pady=5)
        entry_email = tk.Entry(contact_window, font=("Arial", 12), width=30, bg="#252547", fg="white")
        entry_email.pack(pady=5)

        def save_new_contact():
            name = entry_name.get()
            phone = entry_phone.get()
            email = entry_email.get()
            if name and phone and email:
                self.manager.add_contact(name, phone, email)
                self.load_contact_listbox()
                contact_window.destroy()
            else:
                messagebox.showerror("Error", "All fields must be filled!")

        tk.Button(contact_window, text="Save", font=("Arial", 12), bg="#00e676", fg="white", command=save_new_contact).pack(pady=10)

    # Edit selected contact
    def edit_contact(self):
        selected_index = self.contact_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No selection", "Please select a contact to edit.")
            return

        index = selected_index[0]
        contact_id = self.manager.get_contacts()[index][0]  # Get the contact's ID
        contact = self.manager.get_contacts()[index]

        contact_window = tk.Toplevel(self.root)
        contact_window.title("Edit Contact")
        contact_window.configure(bg="#1a1a2e")

        tk.Label(contact_window, text="Name:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(pady=5)
        entry_name = tk.Entry(contact_window, font=("Arial", 12), width=30, bg="#252547", fg="white")
        entry_name.pack(pady=5)
        entry_name.insert(0, contact[1])

        tk.Label(contact_window, text="Phone:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(pady=5)
        entry_phone = tk.Entry(contact_window, font=("Arial", 12), width=30, bg="#252547", fg="white")
        entry_phone.pack(pady=5)
        entry_phone.insert(0, contact[2])

        tk.Label(contact_window, text="Email:", bg="#1a1a2e", fg="white", font=("Arial", 12)).pack(pady=5)
        entry_email = tk.Entry(contact_window, font=("Arial", 12), width=30, bg="#252547", fg="white")
        entry_email.pack(pady=5)
        entry_email.insert(0, contact[3])

        def save_edited_contact():
            name = entry_name.get()
            phone = entry_phone.get()
            email = entry_email.get()
            if name and phone and email:
                self.manager.edit_contact(contact_id, name, phone, email)
                self.load_contact_listbox()
                contact_window.destroy()
            else:
                messagebox.showerror("Error", "All fields must be filled!")

        tk.Button(contact_window, text="Save", font=("Arial", 12), bg="#00e676", fg="white", command=save_edited_contact).pack(pady=10)

    # Delete selected contact
    def delete_contact(self):
        selected_index = self.contact_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No selection", "Please select a contact to delete.")
            return

        index = selected_index[0]
        contact_id = self.manager.get_contacts()[index][0]  # Get the contact's ID
        confirmation = messagebox.askyesno("Delete Contact", "Are you sure you want to delete this contact?")
        if confirmation:
            self.manager.delete_contact(contact_id)
            self.load_contact_listbox()

# Initialize the main window
root = tk.Tk()
app = ContactApp(root)
root.mainloop()
