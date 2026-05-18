from auth import AuthSystem
import pandas as pd
import sqlite3 

class ManagementSystem(AuthSystem):
    def __init__(self, db_path):
        AuthSystem.__init__(self, db_path)
        
    def run_app(self):
        print("--- Encrypt Inc. OS ---")
        user = input("Username: ")
        pw = input("Password: ")
        
        # This calls the standard auth check
        user_type, first_name = self.authenticate_user(user, pw)
        
        if user_type:
            print(f"\nLogin Successful! Welcome: {first_name} // ({user_type.upper()})")
            if user_type == "Admin":
                self.admin_interface() 
            else:
                self.talent_interface()
        else:
            print("\nAccess Denied.")

    def admin_interface(self):
        # Continue the admin interface here, allowing admins to view any table and manage records.
        name = input("Enter the table name to display: ")
        self.display_table(name)
        
    def talent_interface(self):
        # Continue the talent interface here, allowing talents to view only their own records.
        print(f"Accessing your records...") 
        # insert query to pull every table with respective names
        def display_table(self, table_name):
            conn, _ = self.connect_database()
            if conn:
                try:
                    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn) # Query here
                    if df.empty:
                        print(f"\n[!] The {table_name} table is currently empty.") 
                    else:
                        print(f"\n--- {table_name} Table ---")
                        # index=False makes it look cleaner in the console
                        print(df.to_string(index=False)) 
                except Exception as e:
                    print(f"Error reading table: {e}")
                finally:
                    conn.close()
        def prop_form():
            # Subroutine for algorithmic form to draft idea proposal
            pass