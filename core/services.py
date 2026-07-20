# core/services.py
import heapq
from .models import Proposal

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
                (Title, ProjectType, Genre, Duration, Desc, EstBudget, SubmittedBy)
                VALUES %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (title, project_type, genre, duration, description, est_budget, username),
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
                print(f"- {title} | Priority Score: {score}")  # next step: push to Projects table in frontend for admin review and approval, then move to Projects table in database
                
            return heap_entry # hide priority score