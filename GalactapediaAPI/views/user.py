"""View module for handling requests about game types"""
from rest_framework.permissions import DjangoModelPermissions
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserView(ViewSet):
    """Stellar Object View"""

    def list(self, request):
        """Handle GET requests for moons

        Returns:
            Response -- JSON serialized moons
        """
        try:
            user = User.objects.get(pk=request.auth.user_id)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for wiki articles

    Arguments:
        serializers
    """
    class Meta:
        model = User
        fields = ('is_staff',)

