from django.contrib import admin

# Register your models here.
from .models import Config, InputFile

admin.site.register(Config)
admin.site.register(InputFile)