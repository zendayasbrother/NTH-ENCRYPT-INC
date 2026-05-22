from auth import AuthSystem
import pandas as pd
import sqlite3 

class ManagementSystem(AuthSystem):
    def __init__(self, db_path):
        super().__init__(db_path)
        
    def run_app(self):
        print("--- Encrypt Inc. OS ---")
        user = input("Username: ")
        pw = input("Password: ")
        
        user_type, first_name = self.authenticate_user(user, pw)
        
        if user_type:
            print(f"\nLogin Successful! Welcome: {first_name} // ({user_type.upper()})")
            # Store current user state for session-like permission verification
            self.current_user = user
            self.current_user_type = user_type
            
            if user_type == "Admin":
                self.admin_interface() 
            else:
                self.talent_interface()
        else:
            print("\nAccess Denied.")


    def admin_interface(self):
        conn, cursor = self.connect_database()
        # Choices before a button and reactions
        while True:
            print("\n--- ADMIN DASHBOARD ---")
            print("1. View Table")
            print("2. Manage Proposals")
            print("3. Exit")
            choice = input("Select an option: ")
            
            if choice == "1":
                name = input("Enter the table name to display: ")
                self.display_table(name) # Safe global call inherited from DataManager
            elif choice == "2":
                print("Accessing creator proposals...")
                # Insert proposal manipulation logic here
                cursor.execute("")
            elif choice == "3":
                break
        
    def talent_interface(self):
        while True:
            print("\n--- TALENT DASHBOARD ---")
            print("1. View My Records")
            print("2. Submit Project Proposal")
            print("3. Exit")
            choice = input("Select an option: ")
            
            if choice == "1":
                self.display_talent_records(self.current_user)
            elif choice == "2":
                self.prop_form()
                # Choice navigation logic here
            elif choice == "3":
                break

    def display_talent_records(self, username):
        conn, _ = self.connect_database()
        if not conn: 
            return
            
        print(f"\n--- Fetching secure records for {username} ---")
        try:
            # Explicitly checking key tables by parameterized username to avoid leaks
            tables_to_check = ['Users', 'ParticipationLedger', 'Proposals']
            
            for table in tables_to_check:
                # Note: Table names are hardcoded safely here; query parameters are protected
                query = f"SELECT * FROM {table} WHERE Username = ?"
                df = pd.read_sql_query(query, conn, params=(username,))
                
                if not df.empty:
                    print(f"\n[Your Data] Table: {table}")
                    print(df.to_string(index=False))
                    
        except Exception as e:
            print(f"Error compiling your workspace: {e}")
        finally:
            conn.close()

    def prop_form(self):
        conn, cursor = self.connect_database()
        if not conn:
            print("[!] Database connection failed.")
            return
        name = self.first_name
        user = self.username
        
        # Algorithmic form
        print("\n--- New Project Proposal Form ---")
        title = input("Project Title: ")
        self.projType = input("Project Type: ")
        self.genre = input("Genre (Action/Comedy/Drama/etc): ")
        self.est_budget = int(input("Estimated Budget (£): "))
        
        try:    
            budget = pd.read_sql_query(f"SELECT Budget FROM Projects", conn)
            max_budget = int(budget['Budget'].max() * 1.25)
            self.genres = pd.read_sql_query(f"SELECT Genre FROM Projects", conn)
            # if statement with "if self.est_budget > max(1.25 * greates budget table by genre): denided, priority and queue pos is based on ideality
            if self.est_budget > max_budget:
                # Denied, re-enter suitable budget
                print(f"Sorry {name}, the budget for this proposal - {title} - exceeds the budget. Please re-enter a lower figure")
                self.est_budget = int(input("Estimated Budget (£): "))
            else:
                # Start loading values into table as INSERT
                print(f"[*] Proposal for '{title}' saved to pending validation queue.")
                cursor.execute("INSERT INTO Proposals VALUES: ")
        except Exception as e:
            print(f"[!] Error calculating financial thresholds: {e}")
        
    