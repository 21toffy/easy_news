import requests
import os
import json
from requests.models import Response as Res
from .models import Items, ParentChilRelationship
import logging
class ItemManager:
    def __init__(self ):
        self.mock_up = True
        self.pre_base_url = os.getenv("PRE_BASE_URL") 
        self.post_base_url = os.getenv("POST_BASE_URL")
        self.get_all_items_url = os.getenv("GET_ALL_ITEMS_URL")


    def error_logs(self, error, item_id, function_name, file_name, other):
        logging.basicConfig(
            level=logging.CRITICAL,
            format="{asctime} {levelname:<8} {message}",
            style= "{",
            filename="mylog.log",
            filemode="w"
        )
        err = logging.critical(f"an error occred in {file_name}, in the {function_name}:::::Item ID:{item_id}:::::::Error:{error}:::Others{other} ")


    def _get(self, item_id, request_type):
        response = None
        try:
            if request_type == 1:
                base_url = self.get_all_items_url
            else:
                if item_id is not None:
                    base_url = self.pre_base_url + str(item_id) + self.post_base_url
            response = requests.get(base_url, headers={"Content-Type": "application/json"})
        except Exception as e:
            self.error_logs(e , item_id, "_get", "managers.py", "_get function on line 36"+ str(e))

        return response


    def fetch_items(self, item_id, request_type):
        response = self._get(item_id, request_type)
        return response


    def fetch_child(self, item_id):
        response = None       
        try:
            api_call = self._get(item_id, 2)
            if api_call.status_code == 200:
                return json.loads(api_call.text)
            else:
                self.error_logs(e , item_id, "fetch_child", "managers.py", "fetch_child function on line 53"+ str(e))
        except Exception as e:
            self.error_logs(e , item_id, "fetch_child", "managers.py", "fetch child line 55"+ str(e))


    def fetch_item(self, item_id):
        response = None       
        try:
            api_call = self._get(item_id, 2)
            if api_call.status_code == 200:
                self.save_item(api_call.text)
            else:
                self.error_logs(e , item_id, "Fetch Item", "managers.py", "fetch_item function on line 64"+ str(e))
        except Exception as e:
            self.error_logs(e , item_id, "Fetch Item", "managers.py", "fetch_item function on line 67"+ str(e))


    def save_parent_chid(self, parent, child):
        try:
            ParentChilRelationship.objects.create(
                parent = parent,
                child =  child
                )
            print("+++++++++++++++++++++++saved++++++++++++++++++++++++")
        except Exception as e:
            self.error_logs(e , "parent " +str(parent) + "child "+ str(child), "save_parent_children", "managers.py", "save_parent_children function on line 78"+ str(e))


    def save_children(self, children_array, story_object):
        for child in children_array:
            data = self.fetch_child(child)
            try:
                comment_object = Items.objects.create(
                by = data.get("by", ""),
                hacker_id = data["id"],
                parent = data.get("parent", ""),
                text = data.get("text", ""),
                time = data["time"],
                type = data["type"],
                hackernews=True
                
            )

                self.save_parent_chid(story_object, comment_object)
            except Exception as e:
                self.error_logs(e , child, "save_children", "managers.py", "save_children function on line 96"+ str(e))


    def save_item(self, data_to_be_saved):
        data_to_be_saved = json.loads(data_to_be_saved)        
        if data_to_be_saved["type"] =="job":
            print("this ia a job new type")

            response = self.save_job(data_to_be_saved)
        if data_to_be_saved["type"] =="story":
            response = self.save_story(data_to_be_saved)
        if data_to_be_saved["type"] =="comment":
            response = self.save_comment(data_to_be_saved)
        if data_to_be_saved["type"] =="poll":
            response = self.save_poll(data_to_be_saved)
        if data_to_be_saved["type"] =="poll_option":
            response = self.save_poll_option(data_to_be_saved)
        return response

    def save_job(self, response_data):
        job_object = Items.objects.create(
            hacker_id = response_data["id"],
            by = response_data.get("by", ""),
            score = response_data["score"],
            text = response_data.get("text", ""),
            time = response_data["time"],
            title = response_data["title"],
            type = response_data["type"],
            url = response_data.get("url", ""),
            hackernews=True
            )

    def save_story(self, response_data):
        story_object = Items.objects.create(
            by = response_data.get("by", ""),
            descendants = response_data["descendants"],
            hacker_id = response_data["id"],
            score = response_data["score"],
            time = response_data["time"],
            title = response_data["title"],
            type = response_data["type"],
            url = response_data.get("url", ""),
            hackernews = True

        )
        if response_data.get("kids", ""):
            self.save_children(response_data["kids"], story_object)

    def save_comment(self, response_data):
        comment_object = Items.objects.create(
            by = response_data.get("by", ""),
            hacker_id = response_data["id"],
            text = response_data.get("text", ""),
            time = response_data["time"],
            type = response_data["type"],
            hackernews = True
        )

    def save_poll(self, response_data):
        poll_object = Items.objects.create(
            by = response_data.get("by", ""),
            descendants = response_data.get("descendants", ""),
            hacker_id = response_data["id"],
            score = response_data["score"],
            text = response_data.get("text", ""),

            time = response_data["time"],
            type = response_data["type"],
            hackernews = True
        )
        if response_data["parts"]:
            for pol_opt in response_data["parts"]:
                fetch_child = self.fetch_item(pol_opt)
                child = self.save_poll_option(fetch_child)
                self.save_parent_chid(poll_object, child)


    def save_poll_option(self, response_data):
        job_object = Items.objects.create(
            hacker_id = response_data["id"],
            by = response_data.get("by", ""),
            parent = response_data.get("parent", ""),
            score = response_data["score"],
            text = response_data.get("text", ""),

            time = response_data["time"],
            type = response_data["type"],
            hackernews = True
            )
        return job_object
        