"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from GalactapediaAPI.models import Stellar_Object


class StellarObjectView(ViewSet):
    """Stellar Object View"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for wiki article

        Returns:
            Response -- JSON serialized wiki article
        """
        try:
            stellar_object = Stellar_Object.objects.get(pk=pk)
            serializer = StellarObjectSerializer(stellar_object, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all wiki articles

        Returns:
            Response -- JSON serialized list of wiki articles
        """
        stellar_objects = Stellar_Object.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = StellarObjectSerializer(
            stellar_objects, many=True, context={'request': request})
        return Response(serializer.data)

class StellarObjectSerializer(serializers.ModelSerializer):
    """JSON serializer for wiki articles

    Arguments:
        serializers
    """
    class Meta:
        model = Stellar_Object
        fields = ('id', 'user','name', 'description','mass', 'radius','discovered_on', 'discovered_by')
