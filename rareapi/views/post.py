from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, Category, RareUser

class PostView(ViewSet):
    """Rare post typesview"""

    def retrieve(self, request, pk):
        """Gets a post by its pk

        Returns:
            Response --  single JSON serialized post dictionary
        """
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def list(self, request):
        """Gets all posts

        Returns:
            Response -- JSON serialized list of posts
        """
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handles POST operations

        Returns:
            Response -- JSON serialized post instance
        """
        user = RareUser.objects.get(pk=request.data["rare_user_id"])
        category = Category.objects.get(pk=request.data["category_id"])
        post = Post.objects.create(
            rare_user_id=user,
            category_id=category,
            title=request.data["title"],
            publication_date=request.data["publication_date"],
            image_url=request.data["image_url"],
            content=request.data["content"],
            approved=request.data["approved"],
        )
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handles PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """
        post = Post.objects.get(pk=pk)
        user = RareUser.objects.get(pk=request.data["rare_user_id"])
        post.rare_user_id=user
        category = Category.objects.get(pk=request.data["category_id"])
        post.category_id=category
        post.title=request.data["title"]
        post.publication_date=request.data["publication_date"]
        post.image_url=request.date["image_url"]
        post.content=request.data["content"]
        post.approved=request.data["approved"]
        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handles DELETE requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('rare_user_id', 'category_id',
                  'title', 'publication_date', 'image_url',
                  'content', 'approved')
        depth = 1
