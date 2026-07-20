from rest_framework import serializers
from .models import Proposal

class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = ['id', 'title', 'project_type', 'genre', 'duration', 'description', 'est_budget', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

    def validate_title(self, value):
        if len(value) > 60:
            raise serializers.ValidationError("Title exceeds 60-character limit.")
        return value

    def validate_description(self, value):
        if len(value) > 250:
            raise serializers.ValidationError("Description exceeds 250-character limit.")
        return value