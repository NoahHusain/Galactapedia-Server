"""View module for handling requests about game types"""
from rest_framework.permissions import DjangoModelPermissions
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from GalactapediaAPI.models import Asteroid, Stellar_Object, stellar_objects


class AsteroidView(ViewSet):
    """Stellar Object View"""

    permission_classes = [ DjangoModelPermissions ]
    queryset = Asteroid.objects.none()

    def retrieve(self, request, pk=None):
        """Handle GET requests for asteroids

        Returns:
            Response -- JSON serialized asteroids
        """
        try:
            asteroid = Asteroid.objects.get(pk=pk)
            serializer = AsteroidSerializer(asteroid, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all asteroids

        Returns:
            Response -- JSON serialized list of asteroids
        """
        asteroids = Asteroid.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = AsteroidSerializer(
            asteroids, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized post instance
        """
        
        asteroid = Asteroid()
        asteroid.stellar_object = request.data["stellar_object"]

        try:
            asteroid.save()
            serializer = AsteroidSerializer(asteroid, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single asteroids

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            asteroid = Asteroid.objects.get(pk=pk)
            asteroid.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Asteroid.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """

        asteroid = Asteroid.objects.get(pk=pk)
        asteroid.stellar_object = request.data["stellar_object"]

        asteroid.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for wiki articles

    Arguments:
        serializers
    """
    class Meta:
        model = User
        fields = ('id', 'username','first_name', 'last_name')
        depth = 1

class StellarObjectSerializer(serializers.ModelSerializer):
    """JSON serializer for wiki articles

    Arguments:
        serializers
    """
    user = UserSerializer(many=False)
    class Meta:
        model = Stellar_Object
        fields = ('id', 'user', 'name', 'description','mass', 'radius','discovered_on', 'discovered_by')
        

class AsteroidSerializer(serializers.ModelSerializer):
    """JSON serializer for asteroids

    Arguments:
        serializers
    """
    stellar_object = StellarObjectSerializer(many=False)
    class Meta:
        model = Asteroid
        fields = ('id', 'stellar_object')
        depth = 1

