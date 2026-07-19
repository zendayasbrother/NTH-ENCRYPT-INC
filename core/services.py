# core/services.py
import heapq
from .models import Proposal

class ProposalPriorityService:
    @staticmethod
    def calculate_priority_score(proposal: Proposal, budget_limit=500000) -> int:
        score = 100
        p_type = proposal.project_type.lower()
        
        if p_type == "tv":
            score -= 0
        elif p_type == "video":
            score -= 10
        elif p_type == "film":
            score -= 20
        else:
            score -= 15

        budget = int(proposal.est_budget)
        score -= min(budget // 10000, 20)
        score -= min(proposal.duration, 10)

        genre_bonus = {"drama": 3, "comedy": 2, "action": 1}
        score += genre_bonus.get(proposal.genre.lower(), 0)

        title_penalty = min(10, len(proposal.title) // 10)
        score -= title_penalty

        return max(0, score)

    @classmethod
    def get_sorted_proposal_queue(cls):
        """Fetches pending proposals from PGSQL and returns them sorted via heapq."""
        pending = Proposal.objects.filter(status="PENDING")
        heap = []

        for counter, prop in enumerate(pending):
            score = cls.calculate_priority_score(prop)
            # Tuple: (-score, counter, proposal_object) to prioritize higher scores
            heapq.heappush(heap, (-score, counter, prop))

        ordered_proposals = []
        while heap:
            neg_score, _, prop = heapq.heappop(heap)
            ordered_proposals.append({
                "proposal": prop,
                "score": -neg_score
            })
        return ordered_proposals