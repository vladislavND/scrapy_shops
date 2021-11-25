from fastapi import APIRouter, Depends
from sqlmodel import Session

from core.db.dependecy import get_db
from core.models.price import PriceBase, PriceIn
from core.crud.price import CRUDPrice
from core.utils.price_parser import PriceShopParser

router = APIRouter()
crud = CRUDPrice()


@router.post('/price', response_model=PriceBase)
def get_price(data: PriceIn, session: Session = Depends(get_db)):
    try:
        url, article = data.url.split('|')
        data = PriceShopParser().compare(url=url, product_id=article)
    except ValueError:
        data = PriceShopParser().compare(url=data.url, product_id=data.rf_article)

    data = PriceBase(**data)
    return crud.create(data, session)

