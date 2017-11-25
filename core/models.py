from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from stdimage import StdImageField
from stdimage.utils import UploadToClassNameDirUUID

# Create your models here.
class User(AbstractUser):
    WORK_IN_OFFICE = 'work in office'
    NOT_WORKING = 'not working'
    WORK_REMOTE = 'work reomte'
    SICK = 'sick'
    BUSY = 'busy'

    STATUS_CHOICES = (
        (WORK_IN_OFFICE, _(WORK_IN_OFFICE)),
        (WORK_REMOTE, _(WORK_REMOTE)),
        (SICK, _(SICK)),
        (BUSY, _(BUSY)),
    )

    status = models.CharField(max_length=20, null=True, blank=True, choices=STATUS_CHOICES)
    comment = models.TextField(null=True, blank=True)
    photo = StdImageField(verbose_name=_("image"), null=True, blank=True, upload_to=UploadToClassNameDirUUID())
    def thumbnail(self):
        return u'<img src="%s%s" />' % (settings.MEDIA_URL, self.image.thumbnail)
    thumbnail.allow_tags = True
    

class Entry(models.Model):
    ENTER = 'enter'
    EXIT = 'exit'

    TYPE_CHOICES = (
        (ENTER, _(ENTER)),
        (EXIT, _(EXIT)),
    )

    user = models.ForeignKey('core.User', null=True, blank=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, null=True, blank=True, choices=TYPE_CHOICES)
    datetimestamp = models.DateTimeField(auto_now_add=True)
    photo = StdImageField(verbose_name=_("image"), null=True, blank=True, upload_to=UploadToClassNameDirUUID())
    def thumbnail(self):
        return u'<img src="%s%s" />' % (settings.MEDIA_URL, self.image.thumbnail)
    thumbnail.allow_tags = True

class Shedule(models.Model):
    user = models.ForeignKey('core.User', null=True, blank=True, on_delete=models.CASCADE)
    day_of_week = models.IntegerField()
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)

class Project(models.Model):
    users = models.ManyToManyField('core.User')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)