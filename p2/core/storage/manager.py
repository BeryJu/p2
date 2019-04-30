"""p2 core storage manager"""
from p2.lib.config import CONFIG
from p2.lib.reflection import class_to_path, path_to_class


def choices():
    """Get list of tuples of (path to class, class name)"""
    from p2.core.storage.base import StorageController
    # Make sure all controllers are imported
    for controller in CONFIG.y('storage.controllers', []):
        path_to_class(controller)
    for klass in StorageController.__subclasses__():
        yield (class_to_path(klass), klass.__name__)
