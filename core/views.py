# Create your views here.
# core/views.py 

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ProposalSerializer
from .services import ProposalPriorityService
from .models import Proposal

# Continue Authentication as View
class ProposalSubmitView(APIView):
    """Replaces prop_form() CLI input loop[cite: 16]"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ProposalSerializer(data=request.data)
        if serializer.is_serializer_valid():
            serializer.save(submitted_by=request.user)
            return Response({"message": "Proposal submitted successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProposalQueueView(APIView):
    """Replaces admin_interface choice #3 / pending proposals queue[cite: 16]"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'ADMIN':
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
            
        queue = ProposalPriorityService.get_priority_queue()
        return Response({"priority_queue": queue}, status=status.HTTP_200_OK)
    

