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

    def prop_form(self):
        conn, cursor = self.connect_database()
        if not conn or not cursor:
            print("[!] Database connection failed.")
            return

        first_name = getattr(self, "current_user_first_name", getattr(self, "first_name", "Creator"))
        username = self.get_current_username()

        print("\n--- New Project Proposal Form ---")
        project_type = self._normalize_project_type(input("Project Type (TV series/Film/Video): ").strip() or "Undefined")
        if not self._validate_project_type(conn, project_type):
            conn.close()
            return

        title = input("Project Title: ").strip() or "Untitled Proposal"
        title = self._validate_title(title, project_type)
        if title is None:
            conn.close()
            return

        genre = input("Genre (Action/Comedy/Drama/etc): ").strip() or "Undefined"

        try:
            duration = int(input("Estimated Duration (in months): "))
        except ValueError:
            print("[!] Duration must be a whole number.")
            conn.close()
            return

        description = input("Brief Description (max 250 characters): ").strip() or "No description provided."
        description = self._validate_description(description)
        if description is None:
            conn.close()
            return

        try:
            est_budget = int(input("Estimated Budget (£): "))
        except ValueError:
            print("[!] Budget must be a whole number.")
            conn.close()
            return

        max_budget = self._get_budget_limit(conn, est_budget, title, first_name)
        if max_budget is None:
            conn.close()
            return

        proposal = SimpleNamespace(
            title=title,
            project_type=project_type,
            genre=genre,
            duration=duration,
            description=description,
            budget=est_budget,
            budget_limit=max_budget,
            submitted_by=username,
        )

        score = self.priority_score(proposal)

        try:
            cursor.execute(
                """
                INSERT INTO Proposals
                (Title, ProjectType, Genre, Duration, Desc, Budget, SubmittedBy, PriorityScore)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (title, project_type, genre, duration, description, est_budget, username, score),
            )
            conn.commit()
            print(f"[*] Proposal for '{title}' saved to pending validation queue.")
            print(f"[*] Priority score: {score}")

        except Exception as e:
            conn.rollback()
            print(f"[!] Error saving proposal: {e}")
        finally:
            conn.close()

    def _normalize_project_type(self, project_type):
        normalized = str(project_type or "").strip().lower()
        if normalized in {"tv", "tv series", "series"}:
            return "tv"
        if normalized in {"video", "video project"}:
            return "video"
        if normalized in {"film", "movie", "feature"}:
            return "film"
        return normalized or "undefined"

    def _validate_project_type(self, conn, project_type):
        proj_type_table = pd.read_sql_query("SELECT ProjectType FROM Projects", conn)
        if proj_type_table.empty:
            allowed_types = {"tv", "video", "film"}
        else:
            allowed_types = {
                self._normalize_project_type(value)
                for value in proj_type_table["ProjectType"].dropna().tolist()
            }
            allowed_types.update({"tv", "video", "film"})

        if project_type not in allowed_types:
            print(f"[!] Project type '{project_type}' is not recognized. Please select TV, Film, or Video.")
            return False
        return True

    def _validate_title(self, title, project_type):
        title = title.strip() or "Untitled Proposal"
        if project_type == "video" and len(title) > 60:
            print("[!] Title exceeds the 60-character limit for video projects.")
            return None
        if len(title) > 30:
            print("[!] Title exceeds the 30-character limit.")
            return None
        return title

    def _validate_description(self, description):
        description = description.strip() or "No description provided."
        if len(description) > 250:
            print("[!] Description exceeds the 250-character limit.")
            return None
        return description

    def _get_budget_limit(self, conn, est_budget, title, first_name):
        budget_table = pd.read_sql_query("SELECT Budget FROM Projects", conn)
        if budget_table.empty:
            return est_budget

        max_budget = int(budget_table["Budget"].max())
        if est_budget > max_budget:
            print(f"Sorry {first_name}, the budget for '{title}' exceeds the approved limit. Please enter a lower figure.")
            return None
        return max_budget

    def priority_score(self, proposal):
        """Calculate a priority score based on project attributes and queue priority rules."""
        budget = int(getattr(proposal, "budget", 0))
        max_budget = getattr(proposal, "budget_limit", None)
        project_type = self._normalize_project_type(getattr(proposal, "project_type", ""))
        genre = str(getattr(proposal, "genre", "")).lower()
        title = str(getattr(proposal, "title", ""))
        duration = int(getattr(proposal, "duration", 0) or 0)

        score = 100

        if project_type == "tv":
            score -= 0
        elif project_type == "video":
            score -= 10
        elif project_type == "film":
            score -= 20
        else:
            score -= 15

        score -= min(budget // 10000, 20)
        score -= min(duration, 10)

        genre_bonus = {"drama": 3, "comedy": 2, "action": 1}
        score += genre_bonus.get(genre, 0)

        title_penalty = min(10, len(title) // 10)
        score -= title_penalty

        if max_budget is not None and max_budget > 0:
            score -= min(5, max(0, budget // max(1000, max_budget // 10)))

        return max(0, score)