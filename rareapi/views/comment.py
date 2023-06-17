from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment, Post, RareUser

class CommentView(ViewSet):

    def retrieve(self, request, pk):

        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]},
            status=status.HTTP_404_NOT_FOUND)

    def list(self, request):

        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):

        post = Post.objects.get(pk=request.data["post"])
        author = RareUser.objects.get(pk=request.data["rareUser"])
        
        comment = Comment.objects.create(
            content=request.data["content"],
            created_on=request.data["createdOn"],
            post=post,
            author=author,
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def update(self, request, pk):

        comment = Comment.objects.get(pk=pk)
        comment.content = request.data["content"]
        comment.created_on = request.data["createdOn"]
        
        post_id = Post.objects.get(pk=request.data["post"])
        comment.post_id = post_id        
        author_id = RareUser.objects.get(pk=request.data["rareUser"])
        comment.author_id = author_id
        comment.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'post_id', 'author_id', 'content', 'created_on')
