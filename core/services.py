# core/services.py - business and algo logic
import heapq
from .models import Proposal

class ProposalPriorityService:
    
    @staticmethod
    def calculate_priority_score(proposal: Proposal) -> int:
        score = 100
        proj_type = proposal.project_type.lower()
        
        # Priority deductions based on project type rules
        if proj_type == "tv":
            score -= 0
        elif proj_type == "video":
            score -= 10
        elif proj_type == "film":
            score -= 20
        else:
            score -= 15

        budget = float(proposal.est_budget)
        score -= min(int(budget // 10000), 20)
        score -= min(proposal.duration, 10)

        genre_bonus = {"drama": 3, "comedy": 2, "action": 1}
        score += genre_bonus.get(proposal.genre.lower(), 0)

        title_penalty = min(10, len(proposal.title) // 10)
        score -= title_penalty

        return max(0, score)

    @classmethod
    def get_priority_queue(cls, tenant):
        """
        Dynamically extracts pending proposals from PostgreSQL, builds an in-memory heap,
        and outputs a sorted priority payload without relying on permanent RAM state.
        """
        pending_proposals = Proposal.objects.filter(tenant=tenant, status="PENDING")
        proposal_heap = []

        for counter, proposal in enumerate(pending_proposals):
            score = cls.calculate_priority_score(proposal)
            # Tuple priority trick: (-score, counter, proposal_obj)
            heapq.heappush(proposal_heap, (-score, counter, proposal))

        sorted_list = []
        while proposal_heap:
            neg_score, _, proposal = heapq.heappop(proposal_heap)
            sorted_list.append({
                "id": proposal.id,
                "title": proposal.title,
                "submitted_by": proposal.submitted_by.username,
                "priority_score": -neg_score,
                "est_budget": proposal.est_budget,
                "created_at": proposal.created_at,
            })
            
        return sorted_list