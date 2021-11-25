from typing import Any, List

from sqlmodel import Session, select

from core.crud.base import CRUDBase
from core.models.shop import Shop, File, FileBase


class CRUDShop(CRUDBase):
    model = Shop






