"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from GalactapediaAPI.models import Stellar_Object


class StellarObjectView(ViewSet):
    """Stellar Object View"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for stellar object

        Returns:
            Response -- JSON serialized stellar object
        """
        try:
            stellar_object = Stellar_Object.objects.get(pk=pk)
            serializer = StellarObjectSerializer(stellar_object, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all stellar object

        Returns:
            Response -- JSON serialized list of stellar object
        """
        stellar_objects = Stellar_Object.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = StellarObjectSerializer(
            stellar_objects, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized post instance
        """

        user = User.objects.get(username=request.auth.user)


        stellar_object = Stellar_Object()
        stellar_object.user = user
        stellar_object.name = request.data["name"]
        stellar_object.description = request.data["description"]
        stellar_object.mass = request.data["mass"]
        stellar_object.radius = request.data["radius"]
        stellar_object.image = request.data["image"]
        stellar_object.discovered_on = request.data["discovered_on"]
        stellar_object.discovered_by = request.data["discovered_by"]

        try:
            stellar_object.save()
            serializer = StellarObjectSerializer(stellar_object, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single stellar object

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            stellar_object = Stellar_Object.objects.get(pk=pk)
            stellar_object.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Stellar_Object.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StellarObjectSerializer(serializers.ModelSerializer):
    """JSON serializer for wiki articles

    Arguments:
        serializers
    """
    class Meta:
        model = Stellar_Object
        fields = ('id', 'user','name', 'description','mass', 'radius','discovered_on', 'discovered_by')
