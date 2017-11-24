import datetime
from django.shortcuts import render
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework import views, viewsets
from rest_framework.parsers import FileUploadParser
from core.serializers import *
import face_recognition

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

    `curl -H "Authorization: Token 512e3026a7c11dc6cc52027a6c1677b012f0dfae" -H "Content-Disposition: attachment; filename=андрюха.png" --data-binary @"../Downloads/андрюха.png" https://absolute.cloud.technokratos.com/api/entries/`
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    parser_classes = (FileUploadParser,)

    def create(self, request, *args, **kwargs):
        # request.data._mutable = True
        request.data['photo'] = request.data['file']
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)

        if not Entry.objects.filter(user=request.user):
            request.data['type'] = 'enter'
        elif Entry.objects.filter(user=request.user, type='enter', datetimestamp__gte=today_min):
            request.data['type'] = 'exit'
        else:
            request.data['type'] = 'enter'

        known_image = face_recognition.load_image_file(request.user.photo)
        unknown_image = face_recognition.load_image_file(request.data['file'])

        known_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

        results = face_recognition.compare_faces([known_encoding], unknown_encoding)

        return super(EntryViewSet, self).create(request, *args, **kwargs)