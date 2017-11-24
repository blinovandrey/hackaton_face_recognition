from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline
from core.models import *

class SheduleInline(NestedStackedInline):
    model = Shedule

@admin.register(User)
class UserAdmin(NestedModelAdmin):
	inlines = [SheduleInline]