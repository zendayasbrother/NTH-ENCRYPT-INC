from auth import AuthSystem
import pandas as pd
import sqlite3
import sys
import heapq
from types import SimpleNamespace

class ManagementSystem(AuthSystem):
    def __init__(self, db_path):
        super().__init__(db_path)
        self.proposal_heap = []
        self.proposal_counter = 0 # Implement corporation code for different companies; E07 for Encrypt 360 (this engine)
        self.current_user = None
        self.current_user_type = None
        self.current_user_first_name = None

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
            print("2. Manage Proposals")
            print("3. Exit")
            choice = input("Select an option: ")
            
            if choice == "1":
                name = input("Enter the table name to display: ")
                if name.lower() == "proposals":
                    print("[!] Note: Proposals are managed through the proposal queue.")
                    name = input("Enter the table name to display: ")
                self.display_table(name) # excluding Proposals for duplicate management
            elif choice == "2":
                print("Accessing creator proposals...")
                cursor.execute("SELECT * FROM Proposals ORDER BY PriorityScore DESC")
            elif choice == "3":
                exit_choice = input("Are you sure you want to exit? (yes/no): ").strip().lower()
                if exit_choice == "yes":
                    print("[*] Exiting Admin Dashboard.")
                    sys.exit(0)
                    break
                elif exit_choice == "no":
                    continue
        
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
            tables_to_check = ['Users', 'Proposals']
            
            for table in tables_to_check:
                query = f"SELECT * FROM {table} WHERE Username = ?" # fiind secondary attribute to display only relevant records for the logged-in user
                df = pd.read_sql_query(query, conn, params=(username,))
                
                if not df.empty:
                    print(f"\n[Your Data] Table: {table}")
                    print(df.to_string(index=False))
                
                # exclude HashedPassword from Users table for security
                if table == 'Users' and not df.empty:
                    df = df.drop(columns=['HashedPassword'], errors='ignore')
                    print(f"\n[Your Data] Table: {table} (Sensitive data excluded)")
                    print(df.to_string(index=False))
                    
        except Exception as e:
            print(f"Error compiling your workspace: {e}")
        finally:
            conn.close()

    def prop_form(self):
        conn, cursor = self.connect_database()
        if not conn or not cursor:
            print("[!] Database connection failed.")
            return

        first_name = getattr(self, "current_user_first_name", getattr(self, "first_name", "Creator"))
        username = self.get_current_username()

        print("\n--- New Project Proposal Form ---")
        title = input("Project Title: ").strip() or "Untitled Proposal"
        project_type = input("Project Type: ").strip() or "Undefined"
        genre = input("Genre (Action/Comedy/Drama/etc): ").strip() or "Undefined"

        try:
            try:
                est_budget = int(input("Estimated Budget (£): "))
            except ValueError:
                print("[!] Budget must be a whole number.")
                conn.close()
                return
            
            budget_table = pd.read_sql_query("SELECT Budget FROM Projects", conn)
            if budget_table.empty:
                max_budget = est_budget
            else:
                max_budget = int(budget_table["Budget"].max()) # ideally 500K across roster; average max budget of 75K

            if est_budget > max_budget:
                print(f"Sorry {first_name}, the budget for '{title}' exceeds the approved limit. Please enter a lower figure.")
                conn.close()
                return
        except Exception as e:
            print(f"[!] Error calculating financial thresholds: {e}")
            conn.close()
            return

        proposal = SimpleNamespace(
            title=title,
            project_type=project_type,
            genre=genre,
            budget=est_budget,
            submitted_by=username,
        )

        self._enqueue_proposal(proposal)
        score = self.priority_score(proposal)
        
        try:
            cursor.execute(
                """
                INSERT INTO Proposals 
                (Title, ProjectType, Genre, Budget, SubmittedBy, PriorityScore) 
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (title, project_type, genre, est_budget, username, score),
            )
            conn.commit()
            print(f"[*] Proposal for '{title}' saved to pending validation queue.")
            print(f"[*] Priority score: {score}")
            
        except Exception as e:
            conn.rollback()
            print(f"[!] Error saving proposal: {e}")
        finally:
            conn.close()
        
    def priority_score(self, proposal):
        """Calculate a priority score based on project attributes and the 
        most similar to existing projects is prioritised"""
        budget = int(getattr(proposal, "budget", 0))
        project_type = str(getattr(proposal, "project_type", "")).lower()
        genre = str(getattr(proposal, "genre", "")).lower()

        # polish scoring logic: x (finalise weighting soon)
        score = 50
        if project_type in {"film", "series", "video"}:
            score += 10
        if genre in {"action", "comedy", "drama"}:
            score += 5
        else:
            score += 2

        score -= min(budget // 10000, 20)
        return score

    def _enqueue_proposal(self, proposal):
        score = self.priority_score(proposal)
        self.proposal_counter += 1
        heap_entry = (-score, self.proposal_counter, proposal)
        heapq.heappush(self.proposal_heap, heap_entry)
        # review_pending_proposals
        if not self.proposal_heap:
            print("[*] No pending proposals.")
            return

        print("\n--- Pending Proposals ---")
        while self.proposal_heap:
            _, _, proposal = heapq.heappop(self.proposal_heap)
            title = getattr(proposal, "title", "Untitled")
            score = self.priority_score(proposal)
            print(f"- {title} | Priority Score: {score}") 
            
        return heap_entry