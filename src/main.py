#!/usr/bin/env python
import uvicorn
from pydantic.dataclasses import dataclass
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from providers import StorageProvider, setup_storage_provider


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # TODO: make this configurable via env vars
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sp = setup_storage_provider()
sp.initialize()

def get_storage_provider():
    # TODO: make this whole shit happen on app startup - so that it happens once
    try:
        # sp = InMemoryProvider(datastore=TREES)
        # sp.initialize()
        yield sp
    finally:
        try:
            pass
            # sp.finalize()
        except NameError:
            pass

# TODO: dehardcode map name
# TODO: embedd map name into lmap and test

@app.post("/")
def store(data: Dict, storage_provider = Depends(get_storage_provider)):
    storage_provider.store("main", data)
    return "ok"


@app.get("/")
def load(storage_provider = Depends(get_storage_provider)):
    return storage_provider.load("main")


if __name__ == "__main__":
    uvicorn.run(app, port=12694, host="0.0.0.0")
