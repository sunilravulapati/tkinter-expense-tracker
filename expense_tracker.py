import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database Setup
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    description TEXT,
    date TEXT
)
""")
conn.commit()

def add_expense():
    amount = amount_entry.get()
    category = category_entry.get()
    description = description_entry.get()
    date = date_entry.get()
    
    if not amount or not category or not date:
        messagebox.showwarning("Input Error", "Please fill in all fields!")
        return
    
    cursor.execute("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                   (amount, category, description, date))
    conn.commit()
    load_expenses()
    clear_entries()

def load_expenses():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM expenses")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def delete_expense():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an expense to delete!")
        return
    for item in selected_item:
        expense_id = tree.item(item)['values'][0]
        cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    load_expenses()

def clear_entries():
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

def on_closing():
    conn.close()
    root.destroy()

# UI Setup
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x400")

# Input Fields
tk.Label(root, text="Amount:").grid(row=0, column=0)
amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1)

tk.Label(root, text="Category:").grid(row=1, column=0)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1)

tk.Label(root, text="Description:").grid(row=2, column=0)
description_entry = tk.Entry(root)
description_entry.grid(row=2, column=1)

tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=3, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=3, column=1)

# Buttons
tk.Button(root, text="Add Expense", command=add_expense).grid(row=4, column=0, columnspan=2)
tk.Button(root, text="Delete Selected", command=delete_expense).grid(row=5, column=0, columnspan=2)

# Expense List
tree = ttk.Treeview(root, columns=("ID", "Amount", "Category", "Description", "Date"), show="headings")
for col in ("ID", "Amount", "Category", "Description", "Date"):
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.grid(row=6, column=0, columnspan=2)

load_expenses()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()