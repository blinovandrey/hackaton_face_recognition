from django.shortcuts import render
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework import views, viewsets

# Create your views here.
class GoogleLoginView(views.APIView):

    def post(self, request, format=None):
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.CLIENT_ID)

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
        except ValueError:
            # Invalid token
            pass