from abc import ABC, abstractmethod
from typing import Dict

from utilities import get_envvar_or_gtfo, gtfo


class StorageProvider(ABC):
    @abstractmethod
    def _initialize(self):
        """A hook for additional per provider startup logic, which is executed just once, when the provider is started"""
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

    def _initialize(self):
        pass

    def load(self, name):
        return self.data[name] 

    def store(self, name, payload):
        self.data[name] = payload


class File(StorageProvider):
    # TODO: implement file provider
    def __init__(self):
        pass

    # def _initialize(self):
        # ...

    # def load(self, name):
        # ...

    # def store(self, name, payload):
        # ...


# TODO: add a contextmanager wrapper for per transaction init / finalize

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
    sp = storage_provider_class(datastore=TREES)

    sp._initialize()
    return sp
