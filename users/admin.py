from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class Admin(admin.ModelAdmin):
    readonly_fields = ('id')

admin.site.register((User))
