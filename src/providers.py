import os
import json
import uuid
import shutil
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

    @staticmethod
    @abstractmethod
    def _requires():
        """What environment variables are required by the provider"""
        pass

    # TODO: handle __init__ to eat variables from _requires


class InMemory(StorageProvider):
    @staticmethod
    def _requires():
        return []

    def __init__(self, datastore: Dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = datastore

    def _initialize(self):
        pass

    def load(self, name):
        return self.data[name] 

    def store(self, name, payload):
        self.data[name] = payload

class File(StorageProvider):
    @staticmethod
    def _requires():
        return [
            "path",
        ]

    # TODO: remove the parameter assigment - see TODO in base class
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: Pathlib
        self.path = path

    def _initialize(self):
        if not os.path.isdir(self.path):
            os.mkdir(self.path)

        try:
            with open(self.path + "/data.json", "r") as f:
                contents = f.read()
        except (FileNotFoundError) as e:
            with open(self.path + "/data.json", "w") as f:
                initial_json_value_as_str = "{}"
                f.write(initial_json_value_as_str)
                contents = initial_json_value_as_str

        try:
            json.loads(contents)
        except (json.decoder.JSONDecodeError) as e:
            corrupted_file_path = self.path + f"/data_corrupted_{uuid.uuid4()}.json"
            shutil.copyfile(self.path + "/data.json", corrupted_file_path)
            print("ERR: detected corrupted JSON")
            print(f"ERR: reverting to default state, the corrupted filie will be in {corrupted_file_path}")

            with open(self.path + "/data.json", "w") as f:
                initial_json_value_as_str = "{}"
                f.write(initial_json_value_as_str)

    def load(self, name):
        with open(self.path + "/data.json", "r") as f:
            maps_data = json.loads(f.read())
            return maps_data[name]

    def store(self, name, payload):
        with open(self.path + "/data.json", "r") as f:
            maps_data = json.loads(f.read())
            maps_data[name] = payload
        with open(self.path + "/data.json.swp", "a+") as f:
            f.write(json.dumps(maps_data))

        shutil.move(self.path + "/data.json.swp", self.path + "/data.json")


# TODO: add a contextmanager wrapper for per transaction init / finalize - is that an overkill?

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

    init_parameters = { parameter: get_envvar_or_gtfo(f"STORAGE_PROVIDER_{storage_provider_class.__qualname__.upper()}_{parameter.upper()}") for parameter in storage_provider_class._requires() }

    # TODO: make it a bit less special case
    if storage_provider_class == InMemory:
        TREES = {}
        init_parameters["datastore"] = TREES

    sp = storage_provider_class(**init_parameters)

    sp._initialize()
    return sp
