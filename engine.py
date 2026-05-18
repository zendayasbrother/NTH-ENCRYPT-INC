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
    
        # Algorithmic form
        print("\n--- New Project Proposal Form ---")
        title = input("Project Title: ")
        projType = input("Project Type: ")
        self.genre = input("Genre (Action/Comedy/Drama/etc): ")
        self.est_budget = int(input("Estimated Budget (£): "))
        
            
        budget = pd.read_sql_query(f"SELECT Budget FROM Projects", conn)
        genres = pd.read_sql_query(f"SELECT Genre FROM Projects", conn)
        # if statement with "if self.est_budget > max(1.5 * greates budget table by genre): denided, elif 1.5 times: bottom priority queue, else: ideal film + pos
        if self.est_budget > (1.25 * max(budget)):
            # Denied, re-enter suitable budget
            pass
        else:
            print(f"[*] Proposal for '{title}' saved to pending validation queue.")
            cursor.execute("UPDATE ")
        
        
    