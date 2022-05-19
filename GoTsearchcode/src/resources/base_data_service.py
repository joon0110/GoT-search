from abc import ABC, abstractmethod
import copy

class BaseDataException():
    def __init__(self):
        pass

class BaseDataService():
    def __init__(self,config_info):
        self.config_info = copy.deepcopy(config_info)
        self.connection = None

    @abstractmethod
    def _get_connection(self):
        """
        :return:
        """
        pass

    @abstractmethod
    def _close_connection(self):
        """
        :return:
        """

    @abstractmethod
    def get_by_template(self,collection_name, template=None, field_list=None):
        pass

    @abstractmethod
    def list_resources(self):
        return
