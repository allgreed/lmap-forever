from abc import ABC, abstractmethod
from typing import Dict

from utilities import get_envvar_or_gtfo, gtfo


class StorageProvider(ABC):
    @abstractmethod
    def initialize(self): 
        """A hook for per provider startup logic"""
        raise NotImplementedError("Please implement this")

    @abstractmethod
    def finalize(self): 
        """A hook for per provider cleanup logic"""
        raise NotImplementedError("Please implement this")

    @abstractmethod
    def load(self, name):
        """Load a map by name"""
        pass

    @abstractmethod
    def store(self, name):
        """Save a map by name"""
        pass


class InMemory(StorageProvider):
    def __init__(self, datastore: Dict):
        self.data = datastore

    def initialize(self):
        pass

    def finalize(self):
        pass

    def load(self, name):
        return self.data[name] 

    def store(self, name, payload):
        self.data[name] = payload


class File(StorageProvider):
    # TODO: implement file provider
    def __init__(self):
        pass

    # def initialize(self):
        # pass

    # def finalize(self):
        # pass

    # def load(self, name):

    # def store(self, name, payload):


def setup_storage_provider():
    user_storage_provider = get_envvar_or_gtfo("STORAGE_PROVIDER_TYPE")

    resolution_table = {
        "memory": InMemory,
        "file": File,
    }

    try:
        storage_provider_class = resolution_table[user_storage_provider]
    except KeyError:
        gtfo(f"There's no provider type matching {user_storage_provider} avaible")

    # TODO: dehardcode, allow more custom provider initialization
    TREES = {}
    return storage_provider_class(datastore=TREES)