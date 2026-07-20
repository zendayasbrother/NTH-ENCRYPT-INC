import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from auth import AuthSystem
import pandas as pd
import psycopg2
import sys
import heapq
from types import SimpleNamespace

load_dotenv()

class DataManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect_database(self):
        if not self.db_path:
            print("Error: Database connection string is empty.")
            return None, None
            
        try:
            # Connect directly to your PostgreSQL instance using the string
            con = psycopg2.connect(self.db_path)
            cursor = con.cursor()
            cursor.execute('SET search_path TO "Notation", public;')
            return con, cursor
        except psycopg2.Error as error:
            print(f"Database connection error: {error}")
            return None, None

    def display_table(self, table_name):
        conn, _ = self.connect_database()
        if conn:
            try:
                # pandas makes SQL results look like a clean spreadsheet
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                
                if df.empty:
                    print(f"\n[!] The {table_name} table is currently empty.")
                else:
                    if table_name.lower() == "users" and 'HashedPassword' in df.columns:
                        df = df.drop(columns=['HashedPassword']) # drops the HashedPassword column for security reasons
                    print(f"\n--- {table_name} Table ---")
                    print(df.to_string(index=False)) 
            except Exception as e:
                print(f"Error reading table: {e}")
            finally:
                conn.close() # edit database accordingly (createdAt timestamps for Proposals and Projects alike)
                

class ManagementSystem(AuthSystem):
    def __init__(self, db_path):
        super().__init__(db_path)
        self.proposal_heap = []
        self.proposal_counter = 0
        self.current_user = None
        self.current_user_type = None
        self.current_user_first_name = None
        self.corpcode = "E07"  # Default corporate code for Encrypt 360

    def get_current_username(self):
        current_user = getattr(self, "current_user", None)
        if current_user:
            return current_user

        username = getattr(self, "username", None)
        if username:
            return username

        return "Unknown"

    def admin_interface(self):
        conn, cursor = self.connect_database()
        # Choices before a button and reactions
        while True:
            print("\n--- ADMIN DASHBOARD ---")
            print("1. View Table")
            print("2. View Records")
            print("3. Manage Proposals")
            print("4. Sign Talent")  # also ability to sign new talent in a similar algorithmic way to the proposal queue
            print("5. Exit")
            choice = input("Select an option: ")
            
            if choice == "1":
                name = input("Enter the table name to display: ")
                if name.lower() == "proposals":
                    print("[!] Note: Proposals are managed through the proposal queue.")
                    name = input("Enter the table name to display: ")
                self.display_table(name) # excluding Proposals for duplicate management
            elif choice == "2": 
                pass
            elif choice == "3":
                print("Accessing creator proposals...")
                df = pd.read_sql_query("SELECT * FROM Proposals", conn) # give admins agency over the order
                print(df)
            elif choice == "4":
                print("Signing new talent...")
                self.sign_talent()
            elif choice == "5":
                exit_choice = input("Are you sure you want to exit? (yes/no): ").strip().lower()
                if exit_choice == "yes":
                    print("[*] Exiting Admin Dashboard.")
                    sys.exit(0)
                    break
                elif exit_choice == "no":
                    continue # subsitutee for UI
    
    def sign_talent(self):
        print("\n--- Sign New Talent ---")
        email = input("Enter talent's email for verification: ")
        username = input("Choose a username for the talent: ")
        password = input("Create Password for the talent: ") # pwinput.pwinput(prompt="Create Password: ", mask="*") then have it hashed
        corpcode = input("Enter your corporate code: ")

        success = self.sign_up(email, username, password)
        if success:
            print(f"[*] Talent '{username}' signed successfully.")
        else:
            print("[!] Talent sign-up failed. Please try again.")
        
    def talent_interface(self):
        while True:
            print("\n--- TALENT DASHBOARD ---")
            print("1. View My Records")
            print("2. Submit Project Proposal")
            print("3. Exit")
            choice = input("Select an option: ") # Choice navigation logic here
            
            if choice == "1":
                self.display_talent_records(self.current_user)
            elif choice == "2":
                self.prop_form()
            elif choice == "3":
                break

    def display_talent_records(self, username):
        conn, _ = self.connect_database()
        if not conn: 
            return
            
        print(f"\n--- Fetching secure records for {username} ---")
        try:
            tables = ["Users", "Projects", "Proposals"] # use df in init() to expand to all tables in the database
            for table in tables:
                query = f"SELECT * FROM {table} WHERE Username = ?" 
                df = pd.read_sql_query(query, conn, params=(username,))
                
                if df.empty:
                    continue  # Skip empty tables
                
                # exclude HashedPassword from Users table for security
                if table == 'Users':
                    df = df.drop(columns=['HashedPassword'], errors='ignore')
                    print(f"\nTable: {table} (Sensitive data excluded)")
                    print(df.to_string(index=False))
                    
        except Exception as e:
            print(f"Error compiling your workspace: {e}")
        finally:
            conn.close()

    