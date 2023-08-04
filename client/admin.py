from django.contrib import admin
from .models import *


# Register your models here.
@admin.register( 
    SubFee,
    DatabaseDetails,
    OneTimeDetails,
    )

class AppAdmin(admin.ModelAdmin):
    pass