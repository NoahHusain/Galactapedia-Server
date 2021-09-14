"""View module for handling requests about game types"""
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from GalactapediaAPI.models import Star


class StarView(ViewSet):
    """Stellar Object View"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for stellar object

        Returns:
            Response -- JSON serialized stellar object
        """
        try:
            star = Star.objects.get(pk=pk)
            serializer = StarSerializer(star, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all stellar object

        Returns:
            Response -- JSON serialized list of stellar object
        """
        stars = Star.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = StarSerializer(
            stars, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized post instance
        """
        
        star = Star()
        star.star_type = request.data["star_type"]
        star.luminosity = request.data["luminosity"]
        star.stellar_object = request.data["stellar_object"]

        try:
            star.save()
            serializer = StarSerializer(star, context={'request': request})
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
            star = Star.objects.get(pk=pk)
            star.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Star.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """

        star = Star.objects.get(pk=pk)
        star.star_type = request.data["star_type"]
        star.luminosity = request.data["luminosity"]
        star.stellar_object = request.data["stellar_object"]

        star.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class StarSerializer(serializers.ModelSerializer):
    """JSON serializer for wiki articles

    Arguments:
        serializers
    """

    class Meta:
        model = Star
        fields = ('id', 'star_type','luminosity', 'stellar_object')
        depth = 1

