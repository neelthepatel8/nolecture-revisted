import requests
import json

class Requester:
    def __init__(self, url: str, request_object={}):
        self.url = url
        self.request_object = request_object if request_object != {} else None

    def request_with_object(self):
        response = requests.post(self.url, json=self.request_object)
        return response.json()
    
    def update_request_object_variable(self, key, new_value):
        self.request_object["variables"][key] = new_value