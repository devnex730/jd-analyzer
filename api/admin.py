from django.contrib import admin
from .models import JDmodel

@admin.register(JDmodel)
class JDmodelAdmin(admin.ModelAdmin):
    list_display = ('role', )