from django.contrib import admin

# Register your models here.
from .models import Config, Article

admin.site.register(Config)
admin.site.register(Article)