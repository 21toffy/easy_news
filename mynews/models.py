from django.db import models
from common.models import BaseModel, ItemBaseModel
from common.models import constants


class Items(BaseModel, ItemBaseModel):
    text =  models.TextField(null=True)
    title =  models.CharField(max_length=constants.MAX_LENGTH, null=True)
    url =  models.CharField(max_length=constants.MAX_LENGTH, null=True)
    descendants = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    parent = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created_at',)

    @property
    def convert_from_unix(self) -> str:
        from datetime import datetime
        try:
            ts = int(self.time)
            converted_time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            return converted_time
        except Exception as e:

            return self.created_at 

    def __str__(self) -> str:
        return "PARENT: "+"Item type: " + str(self.type) + "Item name " + str(self.title)



class ParentChilRelationship(BaseModel):
    parent = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="items_parent")
    child = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="items_child")
    def __str__(self) -> str:
        return "Parent " + str(self.parent.text) + "Child " + str(self.child.title)

     