from fastapi import APIRouter

from core.crud.scrapyd import crud_scrapyd
from core.models.scrapyd import ListSpiders, Schedule, ResponseSchedule, Jobs, StopSpider

router = APIRouter()


@router.get('/scrapyd/{project}', response_model=ListSpiders)
def get_spiders(project: str):
    spiders = crud_scrapyd.listspiders(project)['spiders']

    return spiders


@router.post('/scrapyd/run', response_model=ResponseSchedule)
def run_spider(data: Schedule):
    item = crud_scrapyd.schedule(**data.dict())
    return item


@router.get('/scrapyd/jobs/{project}', response_model=Jobs)
def get_active_spiders(project: str):
    jobs = crud_scrapyd.listjobs(project)
    return jobs


@router.post('/scrapyd/stop')
def stop_spider(data: StopSpider):
    item = crud_scrapyd.cancel(**data.dict())
    return item
