from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(
 ClientDetails,
 AdminDetails,
)

class AppAdmin(admin.ModelAdmin):
    pass