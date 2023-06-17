from rareapi.models import RareUser
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def check_rare_user(request):
    """Checks to see if RareUser has registered in the app yet
    
    Method arguments:
      request -- The full HTTP request object
    """
    
    uid = request.data['uid']
    
    # Use the built-in authentication method to verify
    # authentication returns the rare_user object or None if no user
    rare_user = RareUser.objects.filter(uid=uid).first()
    
    # If authentication was successful, respond with their token
    if rare_user is not None:
      data = {
        'id': rare_user.id,
        'first_name': rare_user.first_name,
        'last_name': rare_user.last_name,
        'bio': rare_user.bio,
        'profile_image_url': rare_user.profile_image_url,
        'email': rare_user.email,
        'created_on': rare_user.created_on,
        'active': rare_user.active,
        'is_staff': rare_user.is_staff,
        'uid': rare_user.uid
      }
      return Response(data)
    else: 
      # Bad login details were provided, so we can't log the rare_user in
      data = {'valid': False}
      return Response(data)
  
@api_view(['POST'])
def register_rare_user(request):
  """Handles the creation of a new registered user in the app
  
  Method arguments:
    request -- The full HTTP request object
  """
  
  #Now save the rare_user info in the the rareapi_rareuser table
  rare_user = RareUser.objects.create(
    first_name = request.data['firstName'],
    last_name = request.data['lastName'],
    bio = request.data['bio'],
    profile_image_url = request.data['profileImageUrl'],
    email = request.data['email'],
    created_on = request.data['createdOn'],
    active = request.data['active'],
    is_staff = request.data['isStaff'],
    uid = request.data['uid']
  )
  
  # Return the rare_user info to the client
  data = {
      'id': rare_user.id,
      'first_name': rare_user.first_name,
      'last_name': rare_user.last_name,
      'bio': rare_user.bio,
      'profile_image_url': rare_user.profile_image_url,
      'email': rare_user.email,
      'created_on': rare_user.created_on,
      'active': rare_user.active,
      'is_staff': rare_user.is_staff,
      'uid': rare_user.uid
  }
  return Response(data)
