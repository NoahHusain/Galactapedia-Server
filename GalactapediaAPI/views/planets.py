"""View module for handling requests about game types"""
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from GalactapediaAPI.models import Planet, Stellar_Object


class PlanetView(ViewSet):
    """Stellar Object View"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for planets

        Returns:
            Response -- JSON serialized planets
        """
        try:
            planet = Planet.objects.get(pk=pk)
            serializer = PlanetSerializer(planet, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all planets

        Returns:
            Response -- JSON serialized list of planets
        """
        planets = Planet.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PlanetSerializer(
            planets, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized post instance
        """
        
        planet = Planet()
        planet.gravity = request.data["gravity"]
        planet.star = request.data["star"]
        planet.stellar_object = request.data["stellar_object"]
        planet.orbital_period = request.data["orbital_period"]
        planet.is_dwarf = request.data["is_dwarf"]


        try:
            planet.save()
            serializer = PlanetSerializer(planet, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single planets

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            planet = Planet.objects.get(pk=pk)
            planet.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Planet.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """

        planet = Planet.objects.get(pk=pk)
        planet.gravity = request.data["gravity"]
        planet.star = request.data["star"]
        planet.stellar_object = request.data["stellar_object"]
        planet.orbital_period = request.data["orbital_period"]
        planet.is_dwarf = request.data["is_dwarf"]

        planet.save()

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
        

class PlanetSerializer(serializers.ModelSerializer):
    """JSON serializer for planets

    Arguments:
        serializers
    """
    stellar_object = StellarObjectSerializer(many=False)
    class Meta:
        model = Planet
        fields = ('id', 'gravity', 'star', 'orbital_period', 'is_dwarf', 'stellar_object')
        depth = 2

