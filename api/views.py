from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

@api_view(['GET'])
def getRoutes(request):
  routes = [
    {'GET': '/api/projects'},
    {'GET': '/api/projects/id'},
    {'POST': '/api/projects/id/vote'},

    {'POST': '/api/users/token'},
    {'POST': '/api/users/token/refresh'},
  ]
  
  return Response(routes)