from django.contrib import admin
from core.models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	pass