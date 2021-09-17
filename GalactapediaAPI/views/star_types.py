"""View module for handling requests about game types"""
from rest_framework.permissions import DjangoModelPermissions
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from GalactapediaAPI.models import Star_Type


class StarTypeView(ViewSet):
    """Stellar Object View"""

    permission_classes = [ DjangoModelPermissions ]
    queryset = Star_Type.objects.none()

    def retrieve(self, request, pk=None):
        """Handle GET requests for startypes

        Returns:
            Response -- JSON serialized startypes
        """
        try:
            startype = Star_Type.objects.get(pk=pk)
            serializer = StarTypeSerializer(startype, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all startypes

        Returns:
            Response -- JSON serialized list of startypes
        """
        startypes = Star_Type.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = StarTypeSerializer(
            startypes, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized post instance
        """
        
        startype = Star_Type()
        startype.type = request.data["type"]

        try:
            startype.save()
            serializer = StarTypeSerializer(startype, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single startypes

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            startype = Star_Type.objects.get(pk=pk)
            startype.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Star_Type.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """

        startype = Star_Type.objects.get(pk=pk)
        startype.type = request.data["type"]

        startype.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class StarTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for startypes

    Arguments:
        serializers
    """

    class Meta:
        model = Star_Type
        fields = ('id', 'type')
        depth = 1

