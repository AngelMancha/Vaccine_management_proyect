"""Superclass for managing storage in JSON files"""
import hashlib
import json
import os

from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class JsonStore():
    """Superclass for managing storage in JSON files"""
    _FILE_PATH = ""
    _ID_FIELD = ""
    _data_list = []
    def __init__( self ):
        self.load()

    def load( self ):
        """Loading data into the datalist"""
        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            self._data_list = []
        except json.JSONDecodeError as exception_raised:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") \
                from exception_raised

    def save( self ):
        """Saves the datalist in the JSON file"""
        try:
            with open(self._FILE_PATH, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise VaccineManagementException("Wrong file or file path") from ex

    def add_item( self, item ):
        """Adds a new item to the datalist and updates the JSON file"""
        self.load()
        self._data_list.append(item.__dict__)
        self.save()

    def find_item( self, key_value, key=None):
        """Finds the first item with the key_value in the datalist"""
        self.load()
        if key is None:
            key = self._ID_FIELD
        for item in self._data_list:
            if item[key] == key_value:
                return item
        return None

    def find_items_list (self, key_value, key=None):
        """Finds all the items with the key_value in the datalist"""
        self.load()
        if key is None:
            key = self._ID_FIELD
        data_list_result = []
        for item in self._data_list:
            if item[key] == key_value:
                data_list_result.append(item)
        return data_list_result

    def delete_json_file( self ):
        """delete the json file"""
        if os.path.isfile(self._FILE_PATH):
            os.remove(self._FILE_PATH)

    def empty_json_file( self ):
        """removes all data from the json file"""
        self._data_list = []
        self.save()

    def data_hash( self ):
        """calculates the md5 hash of the file's content"""
        return hashlib.md5(self._data_list.__str__().encode()).hexdigest()
