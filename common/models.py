from django.db import models
import uuid
import time
from . import constants

 

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class ItemBaseModel(models.Model):
    hacker_id = models.IntegerField(unique=True, null=True)
    type = models.CharField(max_length=constants.MAX_LENGTH, choices=constants.ITEM_CHOICES,)
    by =  models.CharField(max_length=constants.MAX_LENGTH, null=True)
    time = models.CharField(max_length=constants.MAX_LENGTH, null=True)
    dead = models.BooleanField(default=False)
    hackernews = models.BooleanField(default=False)

    class Meta:
        abstract = True



