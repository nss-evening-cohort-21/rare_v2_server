from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import RareUser
from rest_framework.views import APIView


class RareUserView(APIView):
  
  def get(self, request):
    """Gets all users
    
    Returns 
      Response -- single JSON serialized of users
    """
    uid = request.query_params.get('uid')
    rare_users = RareUser.objects.all()
    
    if uid:
        rare_users = rare_users.filter(uid=uid)
    
    serializer = RareUserSerializer(rare_users, many=True)
    return Response(serializer.data)
      

class RareUserSerializer(serializers.ModelSerializer):
      """JSON serializer for rare_users"""
      
      class Meta:
        model = RareUser
        fields = ('id', 'first_name', 'last_name', 'bio', 'profile_image_url', 'email', 'created_on', 'active', 'is_staff', 'uid')
          
    
