from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from core.models.shop import Shop
from core.db.dependecy import get_db
from core.crud.shop import CRUDShop


router = APIRouter()
crud = CRUDShop()


@router.get('/get_all_shops', response_model=List[Shop])
def get_all_shops(session: Session = Depends(get_db)):
    return crud.get_all(session)

