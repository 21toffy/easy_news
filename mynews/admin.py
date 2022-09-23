from django.contrib import admin

# Register your models here.
from .models import Items, ParentChilRelationship

admin.site.register(Items)
admin.site.register(ParentChilRelationship)
