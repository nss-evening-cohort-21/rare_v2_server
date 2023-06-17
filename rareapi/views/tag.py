"""View module for handling requests about tag"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Tag
from django.db.models import Count


class TagView(ViewSet):
    """Level up tag view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single tag
        Returns:
            Response -- JSON serialized tag
        """
        tag = Tag.objects.annotate.get(pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all tags
        Returns:
            Response -- JSON serialized list of tags
        """

        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
        Response -- JSON serialized Tag instance
        """

        tag = Tag.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"]
        )
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a Tag

        Returns:
        Response -- Empty body with 204 status code
        """

        tag = Tag.objects.get(pk=pk)
        tag.name = request.data["name"]
        tag.age = request.data["age"]
        tag.bio = request.data["bio"]
        tag.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for Tags
    """
    song_count = serializers.IntegerField(default=None)

    class Meta:
        model = Tag
        fields = ('id', "name", "age",
                  "bio", "song_count", "songs")

        depth = 2
