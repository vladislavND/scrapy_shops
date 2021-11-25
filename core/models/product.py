import datetime
from typing import Optional, List
from decimal import Decimal

from sqlmodel import SQLModel, Field, Relationship

from core.models.shop import Shop


class ProductBase(SQLModel):
    name: str
    article: int
    price: Optional[Decimal] = None
    sale_price: Optional[Decimal] = None
    weight: Optional[str] = None
    unit: Optional[str] = None
    date: datetime.date = datetime.date.today()
    shop_id: Optional[int] = Field(default=None, foreign_key='shop.id')
    shop: List[Shop] = Relationship(back_populates="products")


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)






















