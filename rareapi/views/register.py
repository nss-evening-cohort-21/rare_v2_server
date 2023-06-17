from rareapi.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def check_user(request):
    """Checks to see if User has registered in the app yet
    
    Method arguments:
      request -- The full HTTP request object
    """
    
    uid = request.data['uid']
    
    # Use the built-in authentication method to verify
    # authentication returns the user object or None if no user
    user = User.objects.filter(uid=uid).first()
    
    # If authentication was successful, respon with their token
    if user is not None:
      data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'username': user.username,
        'password': user.password,
        'is_staff': user.is_staff,
        'uid': user.uid
      }
      return Response(data)
    else: 
      # Bad login details were provided, so we can't log the user in
      data = {'valid': False}
      return Response(data)
  
@api_view(['POST'])
def register_user(request):
  """Handles the creation of a new registered user in the app
  
  Method arguments:
    request -- The full HTTP request object
  """
  
  #Now save the user infor in the the rareapi_user table   

