import datetime
from typing import Optional
from decimal import Decimal

from sqlmodel import SQLModel, Field
from pydantic import root_validator


class ProcessedProductBase(SQLModel):
    price_rf_kg: Optional[Decimal] = None
    price_rf: Optional[Decimal] = None
    date: datetime.date = datetime.date.today()
    product_article: int
    article_rf: str
    shop_id: Optional[int] = Field(default=None, foreign_key='shop.id')


class ProcessedProduct(ProcessedProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ProcessedAnalise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price_rf: Optional[Decimal] = 0
    price_rf_kg: Optional[Decimal] = 0
    product_price: Optional[Decimal] = 0
    sale_price: Optional[Decimal] = 0
    product_price_kg: Optional[Decimal] = 0
    different_price: Optional[Decimal] = 0
    weight: Optional[str] = None
    unit: Optional[str] = None
    product_article: int
    article_rf: str
    shop_id: int = Field(default=None, foreign_key='shop.id')
    date: datetime.date = datetime.date.today()

    @root_validator
    def price_to_kg(cls, values):
        if values['unit'] in ['г', 'кг']:
            if values['sale_price']:
                price_kg = Decimal(values['sale_price']) / Decimal(values['weight'])
                values['product_price_kg'] = price_kg
                return values
            price_kg = Decimal(values['product_price']) / Decimal(values['weight'])
            values['product_price_kg'] = price_kg
        return values

    @root_validator
    def calc_difference(cls, values):
        if values['product_price_kg']:
            values['different_price'] = values['product_price_kg'] - values['price_rf_kg']
        values['different_price'] = values.get('product_price') - values.get('price_rf')

        return values




