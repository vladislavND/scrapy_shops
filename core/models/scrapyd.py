from typing import List, Any
from datetime import datetime

from pydantic import BaseModel


class Schedule(BaseModel):
    spider: str
    project: str = "parsing"


class ResponseSchedule(BaseModel):
    status: str
    jobid: str


class ListSpiders(BaseModel):
    __root__: List[str]


class Running(BaseModel):
    spider: str
    pid: str
    start_time: datetime
    id: str


class Finished(BaseModel):
    spider: str


class Jobs(BaseModel):
    running: List[Running]
    finished: List[Finished]


class StopSpider(BaseModel):
    job: str
    project: str = 'parsing'

