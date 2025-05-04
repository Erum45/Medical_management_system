import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="user",
        password="*********",
        database="medical_management"
    )

# Function to add patient
def add_patient():
    name = entry_name.get()
    age = entry_age.get()
    gender = entry_gender.get()
    contact = entry_contact.get()

    if name and age and gender and contact:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO patients (name, age, gender, contact) VALUES (%s, %s, %s, %s)", 
                       (name, age, gender, contact))
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Patient added successfully!")
        clear_entries()
        view_patients()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")

# Function to view patients
def view_patients():
    for row in tree.get_children():
        tree.delete(row)
    
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients")
    records = cursor.fetchall()
    db.close()

    for record in records:
        tree.insert("", tk.END, values=record)

# Function to clear input fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_contact.delete(0, tk.END)

# Function to update patient
def update_patient():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a patient to update.")
        return

    patient_id = tree.item(selected_item)['values'][0]
    name = entry_name.get()
    age = entry_age.get()
    gender = entry_gender.get()
    contact = entry_contact.get()

    if name and age and gender and contact:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("UPDATE patients SET name=%s, age=%s, gender=%s, contact=%s WHERE id=%s", 
                       (name, age, gender, contact, patient_id))
        db.commit()
        db.close()
        messagebox.showinfo("Success", "Patient updated successfully!")
        clear_entries()
        view_patients()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")

# Function to delete patient
def delete_patient():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a patient to delete.")
        return

    patient_id = tree.item(selected_item)['values'][0]
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM patients WHERE id=%s", (patient_id,))
    db.commit()
    db.close()
    messagebox.showinfo("Success", "Patient deleted successfully!")
    view_patients()

# Function to search patients
def search_patients():
    search_term = entry_search.get()
    for row in tree.get_children():
        tree.delete(row)

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients WHERE name LIKE %s", ('%' + search_term + '%',))
    records = cursor.fetchall()
    db.close()

    for record in records:
        tree.insert("", tk.END, values=record)

# Create main window
root = tk.Tk()
root.title("Medical Management System")
root.geometry("800x600")
root.configure(bg="#ADD8E6")  # Light blue background

# Create a title label
title_label = tk.Label(root, text="Medical Management System", font=("Helvetica", 24, "bold"), bg="#ADD8E6", fg="#ffffff")
title_label.pack(pady=20)

# Create a frame for input fields
frame_input = tk.Frame(root, bg="#B2EBF2", bd=2, relief=tk.GROOVE)  # Light cyan frame
frame_input.pack(pady=20, padx=20, fill=tk.X)
frame_input.grid_columnconfigure(0, weight=1)
frame_input.grid_columnconfigure(2, weight=1)

# Create input fields with labels
tk.Label(frame_input, text="Name", bg="#B2EBF2", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_name = tk.Entry(frame_input, font=("Helvetica", 12), bd=2, relief=tk.SUNKEN)
entry_name.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame_input, text="Age", bg="#B2EBF2", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_age = tk.Entry(frame_input, font=("Helvetica", 12), bd=2, relief=tk.SUNKEN)
entry_age.grid(row=1, column=1, padx=10, pady=10)

tk.Label(frame_input, text="Gender", bg="#B2EBF2", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_gender = tk.Entry(frame_input, font=("Helvetica", 12), bd=2, relief=tk.SUNKEN)
entry_gender.grid(row=2, column=1, padx=10, pady=10)

tk.Label(frame_input, text="Contact", bg="#B2EBF2", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
entry_contact = tk.Entry(frame_input, font=("Helvetica", 12), bd=2, relief=tk.SUNKEN)
entry_contact.grid(row=3, column=1, padx=10, pady=10)

# Create a frame for buttons
btn_frame = tk.Frame(root, bg="#ADD8E6")  # Matches window background
btn_frame.pack(pady=10)

# Add buttons for CRUD operations with updated colors
btn_add = tk.Button(btn_frame, text="Add Patient", command=add_patient, bg="#81C784", fg="white", font=("Helvetica", 12), bd=0, padx=10, pady=5)
btn_add.grid(row=0, column=0, padx=10)

btn_update = tk.Button(btn_frame, text="Update Patient", command=update_patient, bg="#FFD54F", fg="black", font=("Helvetica", 12), bd=0, padx=10, pady=5)
btn_update.grid(row=0, column=1, padx=10)

btn_delete = tk.Button(btn_frame, text="Delete Patient", command=delete_patient, bg="#E57373", fg="white", font=("Helvetica", 12), bd=0, padx=10, pady=5)
btn_delete.grid(row=0, column=2, padx=10)

btn_view = tk.Button(btn_frame, text="View All Patients", command=view_patients, bg="#64B5F6", fg="white", font=("Helvetica", 12), bd=0, padx=10, pady=5)
btn_view.grid(row=0, column=3, padx=10)

# Search bar for finding patients
entry_search = tk.Entry(btn_frame, font=("Helvetica", 12), bd=2, relief=tk.SUNKEN)
entry_search.grid(row=0, column=4, padx=10, pady=5)
btn_search = tk.Button(btn_frame, text="Search", command=search_patients, bg="#4DB6AC", fg="white", font=("Helvetica", 12), bd=0, padx=10, pady=5)
btn_search.grid(row=0, column=5, padx=10)

# Create a Treeview to display patients
columns = ("ID", "Name", "Age", "Gender", "Contact")
tree = ttk.Treeview(root, columns=columns, show="headings", height=18)
tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Define headings for the columns
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER, width=120)

# Styling for Treeview
style = ttk.Style()
style.configure("Treeview", font=("Helvetica", 12), rowheight= 27, background="#ffffff", fieldbackground="#ffffff")
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#00796b", foreground="#ffffff")
style.map("Treeview", background=[("selected", "#b2dfdb")], foreground=[("selected", "black")])

# Run the main event loop
root.mainloop()
