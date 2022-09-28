from django.contrib import admin

# Register your models here.
from tutorial.models import Orders, Package

admin.site.register(Orders)
admin.site.register(Package)
