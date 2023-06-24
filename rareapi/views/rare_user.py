from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import RareUser

class RareUserView(ViewSet):
  """Rare User typesview"""
  
  def retrieve(self, request, pk):
    """Handle GET request for a single user
    
    Returns 
      Response -- single JSON serialized user
    """
    
    try:
      rare_user = RareUser.objects.get(pk=pk)
      serializer = RareUserSerializer(rare_user)
      return Response(serializer.data)
    except RareUser.DoesNotExist as ex:
      return Response({'message': ex.args[0]},status=status.HTTP_404_NOT_FOUND)
    
    
class RareUserSerializer(serializers.ModelSerializer):
      """JSON serializer for rare_users"""
      
      class Meta:
        model = RareUser
        fields = ('id', 'first_name', 'last_name', 'bio', 'profile_image_url', 'email', 'created_on', 'active', 'is_staff', 'uid')
          
    
