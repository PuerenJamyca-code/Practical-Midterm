import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class DatabaseManager:

    def __init__(self, db_name="profiles.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS person_profiles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        full_name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        city TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        occupation TEXT NOT NULL
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Initialization failed: {e}")

    def add_profile(self, full_name, email, phone, city, age, occupation):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO person_profiles (full_name, email, phone, city, age, occupation)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (full_name, email, phone, city, age, occupation))
                conn.commit()
                return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not insert record: {e}")
            return False

    def fetch_all_profiles(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM person_profiles")
                return cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch records: {e}")
            return []

    def update_profile(self, profile_id, full_name, email, phone, city, age, occupation):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE person_profiles
                    SET full_name = ?, email = ?, phone = ?, city = ?, age = ?, occupation = ?
                    WHERE id = ?
                """, (full_name, email, phone, city, age, occupation, profile_id))
                conn.commit()
                return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not update record: {e}")
            return False

    def delete_profile(self, profile_id):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM person_profiles WHERE id = ?", (profile_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not delete record: {e}")
            return False

    def search_profiles(self, query):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                search_term = f"%{query}%"
                cursor.execute("""
                    SELECT * FROM person_profiles
                    WHERE full_name LIKE ? OR city LIKE ? OR occupation LIKE ?
                """, (search_term, search_term, search_term))
                return cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Search failed: {e}")
            return []


class PersonProfileApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Person Profile Management System")
        self.geometry("950x600")
        self.minsize(850, 500)

        self.db = DatabaseManager()

        self.selected_profile_id = None

        self.create_styles()
        self.create_widgets()

        self.display_profiles()

    def create_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold"),
            padding=6
        )

        self.style.configure(
            "Treeview",
            rowheight=26,
            font=("Arial", 9)
        )

    def create_widgets(self):
        title_label = tk.Label(
            self,
            text="Person Profile Management System",
            font=("Arial", 18, "bold")
        )
        title_label.pack(side="top", fill="x", pady=10)

        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        left_pane = tk.LabelFrame(
            main_frame,
            text=" Profile Information ",
            font=("Arial", 11, "bold"),
            bd=2,
            relief="groove"
        )
        left_pane.pack(side="left", fill="y", padx=(0, 10), pady=5)

        fields = [
            ("Full Name:", "name_entry"),
            ("Email Address:", "email_entry"),
            ("Phone Number:", "phone_entry"),
            ("City:", "city_entry"),
            ("Age:", "age_entry"),
            ("Occupation:", "occupation_entry")
        ]

        for idx, (label_text, attr_name) in enumerate(fields):
            lbl = tk.Label(
                left_pane,
                text=label_text,
                font=("Arial", 10, "bold")
            )
            lbl.grid(row=idx, column=0, padx=10, pady=8, sticky="e")

            entry = tk.Entry(
                left_pane,
                width=26,
                font=("Arial", 10),
                relief="solid",
                bd=1
            )
            
