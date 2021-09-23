"""View module for handling requests about game types"""
from rest_framework.permissions import DjangoModelPermissions
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from GalactapediaAPI.models import Stellar_Object, Star, Planet, Asteroid, Moon, Star_Type
from django.core.files.base import ContentFile
import base64
import uuid




class StellarObjectView(ViewSet):
    """Stellar Object View"""

    permission_classes = [ DjangoModelPermissions ]
    queryset = Stellar_Object.objects.none()

    def retrieve(self, request, pk=None):
        """Handle GET requests for stellar object

        Returns:
            Response -- JSON serialized stellar object
        """
        res_data = None

        try:
            stellar_object = Stellar_Object.objects.get(pk=pk)
            try:
                res_data = Star.objects.get(stellar_object=stellar_object)
                res_data = StarSerializer(res_data, context={'request': request})
            except:
                pass
            try:
                res_data = Planet.objects.get(stellar_object=stellar_object)
                res_data = PlanetSerializer(res_data, context={'request': request})
            except:
                pass
            try:
                res_data = Asteroid.objects.get(stellar_object=stellar_object)
                res_data = AsteroidSerializer(res_data, context={'request': request})
            except:
                pass
            try:
                res_data = Moon.objects.get(stellar_object=stellar_object)
                res_data = MoonSerializer(res_data, context={'request': request})
            except:
                pass

            return Response(res_data.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all stellar object

        Returns:
            Response -- JSON serialized list of stellar object
        """
        stellar_objects = Stellar_Object.objects.all()

        search_text = self.request.query_params.get('name', None)

        if search_text is not None:
            stellar_object = Stellar_Object.objects.get(name=search_text)
            serializer = StellarObjectSerializer(
            stellar_object, many=False, context={'request': request})
            return Response(serializer.data)

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
        stellar_object_type = request.data["type"]

        user = User.objects.get(username=request.auth.user)

        stellar_object = Stellar_Object()
        stellar_object.user = user
        stellar_object.name = request.data["name"]
        stellar_object.description = request.data["description"]
        stellar_object.mass = request.data["mass"]
        stellar_object.radius = request.data["radius"]
        format, imgstr = request.data["image_url"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["name"]}-{uuid.uuid4()}.{ext}')
        stellar_object.image = data
        stellar_object.discovered_on = request.data["discovered_on"]
        stellar_object.discovered_by = request.data["discovered_by"]

        try:
            stellar_object.save()
            attached_stellar_object = Stellar_Object.objects.get(name=request.data['name'])

            if stellar_object_type == "Star":
                star_type = Star_Type()
                star_type.type = request.data["star_type"]
                star_type.save()
                star = Star()
                star.star_type = Star_Type.objects.get(type=request.data['star_type'])
                star.stellar_object = attached_stellar_object
                star.luminosity = request.data["luminosity"]
                star.save()

                
                
            if stellar_object_type == "Planet":
                planet = Planet()
                planet.gravity = request.data["gravity"]
                planet.star_id = request.data["parent_star"]
                planet.orbital_period = request.data["orbital_period"]
                planet.is_dwarf = request.data["is_dwarf"]
                planet.stellar_object = attached_stellar_object
                planet.save()

            if stellar_object_type == "Moon":
                moon = Moon()
                moon.orbital_period = request.data["orbital_period"]
                moon.gravity = request.data["gravity"]
                moon.planet_id = request.data["parent_planet"]
                moon.stellar_object = attached_stellar_object
                moon.save()


            if stellar_object_type == "Asteroid":
                asteroid = Asteroid()
                asteroid.stellar_object = attached_stellar_object
                asteroid.save()

                
                
            serializer = StellarObjectSerializer(
                stellar_object, context={'request': request})
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

    def update(self, request, pk=None):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """

        stellar_object = Stellar_Object.objects.get(pk=pk)
        stellar_object.name = request.data["name"]
        stellar_object.description = request.data["description"]
        stellar_object.mass = request.data["mass"]
        stellar_object.radius = request.data["radius"]
        # stellar_object.image = request.data["image"]
        stellar_object.discovered_on = request.data["discovered_on"]
        stellar_object.discovered_by = request.data["discovered_by"]

        stellar_object.save()

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
        fields = ('id', 'username', 'first_name', 'last_name')
        depth = 1


class StellarObjectSerializer(serializers.ModelSerializer):
    """JSON serializer for wiki articles

    Arguments:
        serializers
    """
    user = UserSerializer(many=False)

    class Meta:
        model = Stellar_Object
        fields = ('id', 'user', 'name', 'description', 'mass',
                  'radius', 'discovered_on', 'discovered_by', 'image')

class StarSerializer(serializers.ModelSerializer):
    """JSON serializer for wiki articles

    Arguments:
        serializers
    """
    stellar_object = StellarObjectSerializer(many=False)
    class Meta:
        model = Star
        fields = ('id', 'star_type', 'luminosity', 'stellar_object')
        depth = 1

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

class MoonSerializer(serializers.ModelSerializer):
    """JSON serializer for moons

    Arguments:
        serializers
    """
    stellar_object = StellarObjectSerializer(many=False)
    class Meta:
        model = Moon
        fields = ('id', 'gravity', 'planet', 'orbital_period', 'stellar_object')
        depth = 2

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
