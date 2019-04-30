"""p2 core manager"""
from p2.lib.config import CONFIG
from p2.lib.reflection import class_to_path, path_to_class


class Manager:
    """Central manager of storage and component controllers"""

    __is_initialized = False

    def init(self):
        """Import all classes specified in config"""
        if not self.__is_initialized:
            # Make sure all controllers are imported
            for controller in CONFIG.y('storage.controllers', []):
                path_to_class(controller)
            # Make sure all controllers are imported
            for controller in CONFIG.y('component.controllers', []):
                path_to_class(controller)
            self.__is_initialized = True

    def storage_controller_choices(self):
        """Get list of tuples of (path to class, class name)"""
        from p2.core.storages.base import StorageController
        self.init()
        for klass in StorageController.__subclasses__():
            yield (class_to_path(klass), klass.__name__)

    def component_controller_choices(self):
        """Get list of tuples of (path to class, class name)"""
        from p2.core.components.base import ComponentController
        self.init()
        for klass in ComponentController.__subclasses__():
            yield (class_to_path(klass), klass.__name__)

    def component_controller_list(self):
        """Get list of all Component Controller classes"""
        from p2.core.components.base import ComponentController
        self.init()
        for klass in ComponentController.__subclasses__():
            yield klass

MANAGER = Manager()
