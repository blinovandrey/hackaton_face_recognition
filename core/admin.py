from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline
from core.models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from push_notifications.models import APNSDevice, GCMDevice, WNSDevice


class SheduleInline(NestedStackedInline):
    model = Shedule


@admin.register(User)
class UserAdmin(NestedModelAdmin):
	inlines = [SheduleInline]


admin.site.unregister(Token)
admin.site.unregister(Group)
admin.site.unregister(APNSDevice)
admin.site.unregister(GCMDevice)
admin.site.unregister(WNSDevice)