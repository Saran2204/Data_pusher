from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
import requests

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

@api_view(['POST'])
def handle_incoming_data(request):
    token = request.headers.get('CL-X-TOKEN')
    if not token:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        account = Account.objects.get(app_secret_token=token)
    except Account.DoesNotExist:
        return Response({"error": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data
    for destination in account.destinations.all():
        headers = destination.headers
        method = destination.http_method.lower()
        url = destination.url
        
        if method == 'get':
            response = requests.get(url, headers=headers, params=data)
        elif method in ['post', 'put']:
            response = getattr(requests, method)(url, headers=headers, json=data)
        
        # Handle response if needed

    return Response({"status": "success"}, status=status.HTTP_200_OK)

def homepage(request):
    return HttpResponse("Welcome to the Data Pusher Application")
