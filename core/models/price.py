import datetime
from typing import Optional
from decimal import Decimal

from sqlmodel import SQLModel, Field


class PriceBase(SQLModel):
    url: str
    shop: str
    article: str
    name: str
    price: Decimal
    sale_price: Optional[Decimal] = None
    different_price: Optional[Decimal] = None
    date: datetime.date = datetime.date.today()


class Price(PriceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class PriceIn(SQLModel):
    url: str
    rf_article: Optional[str] = None
