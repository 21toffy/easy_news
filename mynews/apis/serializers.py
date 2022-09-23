from rest_framework import serializers
from mynews.models import (Items, ParentChilRelationship)

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = (
        "convert_from_unix",
        "hacker_id",
        "type",
        "by",
        "text",
        "title",
        "url",
        "score",
        )
    


