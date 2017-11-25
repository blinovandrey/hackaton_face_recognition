import datetime
import json
from django.shortcuts import render
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework import views, viewsets, mixins
from rest_framework.parsers import FileUploadParser
from core.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from rest_framework.decorators import detail_route

import face_recognition

# Create your views here.
class GoogleLoginView(views.APIView):

    def post(self, request, format=None):
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            userid = idinfo['sub']
        except ValueError:
            pass


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet,):
    """
    Доступ к текущему пользователю: `/users/me/` \n
    Получить токен: `/auth-token/`, username = `email`, password = `password` \n
    Авторизация по токену: `curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'`
    """

    serializer_class = UserSerializer
    queryset = User.objects.none()

    def dispatch(self, request, *args, **kwargs):
        self.perform_authentication(self.initialize_request(request, *args, **kwargs))
        if kwargs.get('pk') == 'me' and request.user:
            kwargs['pk'] = request.user.pk
        return super(UserViewSet, self).dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            validators.validate_email(request.data['email'])
        except:
            raise ValidationError({"email": _('Enter a valid email address.')})
        if User.objects.filter(email=request.data['email']).count() > 0:
            raise ValidationError({"email": _('Email is already registered')})
        if not request.data.get('password', None):
            raise ValidationError({"password": _('Password must be present')})
        if len(request.data['password']) < 6:
            raise ValidationError({"password": _('Password is too short')})
        if not request.data.get('first_name', None):
            raise ValidationError({"first_name": _('Name must be present')})
        user = User.objects.create_user(
            request.data['username'],
            request.data['email'],
            request.data['password'],
            first_name=request.data.get('first_name',""),
            last_name=request.data.get('first_name',""),
            status=request.data.get("status"),
            photo=request.data.get("photo")
        )
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if kwargs.get('pk') == request.user.pk:
            user = User.objects.get(pk=request.user.pk)
            if not user.status in ('work in office', 'not working'):
                user.status = request.data['status']
                user.comment = request.data['comment']
                user.save()
                Entry.objects.create(user=user,type=request.data['status']).save()
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response([_('Wrong credentials')], status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            return User.objects.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
        else:
            return User.objects.all()

    @detail_route(methods=['get'])
    def entries(self, request, pk=None):
        user = self.get_object()
        entries = user.entry_set
        dt_start = request.GET.get('start')
        if dt_start:
            entries = entries.filter(datetimestamp__gte=dt_start)
        dt_end = request.GET.get('end')
        if dt_end:
            entries = entries.filter(datetimestamp__lte=dt_end)
        return Response(EntrySerializer(entries, many=True).data, status=status.HTTP_200_OK)
        

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

        entry = Entry.objects.create(user=None, type=None, photo=request.data['photo'])

        unknown_image = face_recognition.load_image_file(request.data['file'])
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

        for user in User.objects.all():
            if user.photo:
                known_image = face_recognition.load_image_file(user.photo)
                known_encoding = face_recognition.face_encodings(known_image)[0]
                results = face_recognition.compare_faces([known_encoding], unknown_encoding)
                print(results)
                if results[0]:
                    entry.user = user
                    print(entry.user)
                    if not Entry.objects.filter(user=user):
                        entry.type = 'enter'
                        user.status = 'work in office'
                    elif Entry.objects.filter(user=user, type='enter', datetimestamp__gte=today_min):
                        entry.type = 'exit'
                        user.status = 'not working'
                    else:
                        entry.type = 'enter'
                        user.status = 'work in office'
                    entry.save()
                    user.save()
                    break
        return Response(EntrySerializer(entry).data)
