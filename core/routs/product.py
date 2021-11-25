from typing import List
import io

from fastapi import APIRouter, Depends
from sqlmodel import Session
from starlette.responses import StreamingResponse

from core.models.product import Product
from core.db.dependecy import get_db
from core.crud.porduct import CRUDProduct


router = APIRouter()
crud = CRUDProduct()


@router.get('/get_all_products', response_model=List[Product])
def get_all_products(session: Session = Depends(get_db)):
    return crud.get_all(session)


@router.get('/get_all_products_by_shop_id/{shop_id}', response_model=List[Product])
def get_all_products_by_shop_id(shop_id: int, session: Session = Depends(get_db)):
    return crud.get_products_by_shop_id(session, shop_id)


@router.get('/get_product/{product_id}', response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_db)):
    return crud.get(session, product_id)


@router.get('/get_file_names_by/{shop_id}', response_model=List[str])
def get_file_names_by_shop_id(shop_id: int, session: Session = Depends(get_db)):
    print(type(shop_id))
    print(shop_id)
    return crud.get_file_names_by_shop_id(session, shop_id)


@router.get('/get_file_by/{name}', response_class=StreamingResponse)
def get_file_by_name(name: str):
    df = crud.get_file_by_name(name)
    to_write = io.BytesIO()
    df.to_excel(to_write, index=False)
    to_write.seek(0)
    return StreamingResponse(to_write, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

