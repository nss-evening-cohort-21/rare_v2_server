from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment, Post, RareUser

class CommentView(ViewSet):
    """Comment View"""
    def retrieve(self, request, pk):
        """get single"""
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]},
            status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """get all"""
        comments = Comment.objects.all()
        post_comments = request.query_params.get('post_id', None)
        if post_comments is not None:
                comments = comments.filter(post_id=post_comments)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        """create"""
        post_id = Post.objects.get(pk=request.data["postId"])
        author_id = RareUser.objects.get(pk=request.data["authorId"])

        comment = Comment.objects.create(
            content=request.data["content"],
            created_on=request.data["createdOn"],
            post_id=post_id,
            author_id=author_id
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def update(self, request, pk):
        """update"""
        comment = Comment.objects.get(pk=pk)
        comment.content = request.data["content"]
        comment.created_on = request.data["createdOn"]

        post_id = Post.objects.get(pk=request.data["postId"])
        comment.post_id = post_id
        author_id = RareUser.objects.get(pk=request.data["authorId"])
        comment.author_id = author_id
        comment.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """delete"""
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
class CommentSerializer(serializers.ModelSerializer):
    """comment serializer"""
    class Meta:
        model = Comment
        fields = ('id', 'post_id', 'author_id', 'content', 'created_on')
