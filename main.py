from fastapi import FastAPI
from sqlmodel import SQLModel, Session
from pydantic import parse_obj_as
from typing import List

from core.routs.product import router as product_router
from core.routs.shop import router as shop_router
from core.routs.processed import router as processed_router
from core.routs.price import router as price_router
from core.routs.scrapyd import router as scrapyd_router
from core.models.shop import Shop

from core.crud.shop import CRUDShop
from core.db.database import engine
from sqlalchemy.exc import IntegrityError

app = FastAPI()
app.include_router(product_router, prefix="/api", tags=["Product"])
app.include_router(shop_router, prefix="/api", tags=['Shop'])
app.include_router(processed_router, prefix='/api', tags=['Processed'])
app.include_router(price_router, prefix='/api', tags=['Price'])
app.include_router(scrapyd_router, prefix='/api', tags=['Scrapyd'])


@app.on_event('startup')
async def create_category(session: Session = Session(engine)):

    SQLModel.metadata.create_all(engine)
    try:
        shops = [
            {'name': 'utkonos', 'url': 'https://utkonos.ru', 'id': 3},
            {'name': 'ecomarket', 'url': 'https://ecomarket.ru', 'id': 2},
            {'name': 'funduchok', 'url': 'https://фундучок.рф', 'id': 1},
            {'name': 'vkusvill', 'url': 'https://vkusvill.ru', 'id': 4},
            {'name': 'wildbress', 'url': 'https://vkusvill.ru', 'id': 5},
            {'name': 'riboedov', 'url': 'https://ryboedov.ru', 'id': 6}
        ]
        CRUDShop().list_create(session=session, objects=parse_obj_as(List[Shop], shops))
    except IntegrityError:
        pass









