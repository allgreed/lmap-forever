#!/usr/bin/env python
import uvicorn
from pydantic.dataclasses import dataclass
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict


TREE = None
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
def store(data: Dict):
    global TREE
    TREE = data
    return "ok"


@app.get("/")
def load():
    return TREE


if __name__ == "__main__":
    uvicorn.run(app, port=12694, host="0.0.0.0")
