from django.shortcuts import render
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework import views, viewsets
from rest_framework.parsers import FileUploadParser
from core.serializers import *

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


class EntryViewSet(viewsets.ModelViewSet):
    """
    Example:

    `curl -H "Authorization: Token 56597cc7d805609de476188be5744c49c553ef05" -H "Content-Disposition: attachment; filename=андрюха.png" - --data-binary @"/Downloads/андрюха.png" http://127.0.0.1:8000/api/entries/`
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    parser_classes = (FileUploadParser,)

    def create(self, request, *args, **kwargs):
        # request.data._mutable = True
        import pdb; pdb.set_trace()
        request.data['user'] = request.user.id
        request.data['photo'] = request.data['file']
        return super(EntryViewSet, self).create(request, *args, **kwargs)