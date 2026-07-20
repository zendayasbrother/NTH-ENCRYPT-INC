# Create your views here.
# core/views.py 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ProposalSerializer
from .services import ProposalPriorityService
from .models import Proposal

class ProposalSubmitView(APIView):
    """Replaces prop_form() CLI input loop."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ProposalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                submitted_by=request.user,
                tenant=request.user.tenant
            )
            return Response(
                {"message": "Proposal submitted successfully!", "data": serializer.data}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProposalQueueView(APIView):
    # replaces Admin's "Manage Proposals"    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'ADMIN':
            return Response({"error": "Unauthorized access. Admin rights required."}, status=status.HTTP_403_FORBIDDEN)
            
        queue = ProposalPriorityService.get_priority_queue(tenant=request.user.tenant)
        return Response({"priority_queue": queue}, status=status.HTTP_200_OK)