from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rareapi.models import Post, Category, RareUser, Comment

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
        user_posts = request.query_params.get('rare_user_id', None)
        if user_posts is not None:
                posts = posts.filter(rare_user_id=user_posts)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handles POST operations

        Returns:
            Response -- JSON serialized post instance
        """
        user = RareUser.objects.get(pk=request.data["rareUserId"])
        category = Category.objects.get(pk=request.data["categoryId"])
        post = Post.objects.create(
            rare_user_id=user,
            category_id=category,
            title=request.data["title"],
            publication_date=request.data["publicationDate"],
            image_url=request.data["imageUrl"],
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
        user = RareUser.objects.get(pk=request.data["rareUserId"])
        post.rare_user_id=user
        category = Category.objects.get(pk=request.data["categoryId"])
        post.category_id=category
        post.title=request.data["title"]
        post.publication_date=request.data["publicationDate"]
        post.image_url=request.data["imageUrl"]
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

    @action(methods=['get'], detail=True)
    def comments(self, request, pk):
        """gets comments for posts"""
        comments = Comment.objects.all()
        post_comments = comments.filter(post_id=pk)

        serializer = CommentSerializer(post_comments, many=True)
        return Response(serializer.data)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post_id', 'author_id', 'content', 'created_on')
        depth = 1

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'rare_user_id', 'category_id',
                  'title', 'publication_date', 'image_url',
                  'content', 'approved')
        depth = 1
