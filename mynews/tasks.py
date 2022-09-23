from __future__ import absolute_import, unicode_literals

from celery import shared_task

import json
from.models import Items
from .managers import ItemManager

@shared_task#(name="get_all_items")
def get_all_items():
    slice_number = 101
    manager =  ItemManager()
    response = manager.fetch_items('', 1)
    cleasned_data = json.loads(response.text)[:slice_number]
    items = list(Items.objects.all().values_list('hacker_id',flat=True))
    if len(items) < 1 :
        for id in cleasned_data:
            if id is not None:
                try:
                    response_data = manager.fetch_item(id)
                except Exception as e:
                    response_data = str(e)
                    manager.error_logs(e , id, "get all items", "tasks.py", "get_all_items function on line 23"+ str(e))
    else:
        non_existent_items = list(set(cleasned_data) - set(items))
        for id in non_existent_items:
            if id is not None:
                try:
                    response_data = manager.fetch_item(id)
                except Exception as e:
                    manager.error_logs(e , id, "get all items", "tasks.py", "get_all_items function on line 35"+ str(e))
                    response_data = str(e)

    return response_data



