"""p2 core manager"""

from p2.lib.config import CONFIG
from p2.lib.reflection import class_to_path, path_to_class

class ControllerManager:
    """Central manager of storage and component controllers"""

    __config_path = ''
    __class_list = []
    __class_path_list = []
    __loaded = False

    def __init__(self, config_path, lazy=False):
        self.__config_path = config_path
        self.__class_list = []
        self.__class_path_list = []
        if not lazy:
            self.__actual_load()

    def __actual_load(self):
        """Make sure classes are loaded"""
        if not self.__loaded:
            # Make sure all controllers are imported
            for controller in CONFIG.y(self.__config_path, []):
                self.__class_list.append(path_to_class(controller))
                self.__class_path_list.append(controller)
            self.__loaded = True

    def __contains__(self, item):
        """Check if item is in subclasses"""
        self.__actual_load()
        if isinstance(item, str):
            return item in self.__class_path_list
        return item in self.__class_list

    def as_choices(self):
        """Get list of tuples of (path to class, class name)"""
        self.__actual_load()
        for cls in self.__class_list:
            yield (class_to_path(cls), cls.__name__)

    def list(self):
        """Get list of all Component Controller classes"""
        self.__actual_load()
        return self.__class_list
