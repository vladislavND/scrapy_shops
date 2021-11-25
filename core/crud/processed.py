from typing import List, ByteString

import pandas as pd
from fastapi.exceptions import HTTPException
from sqlmodel import select

from core.crud.base import CRUDBase
from core.models.processeed import ProcessedProduct, ProcessedAnalise
from core.models.product import Product
from core.db.database import Session, legacy_engine


class CRUDProcessed(CRUDBase):
    model = ProcessedProduct
    analise_model = ProcessedAnalise

    def add_processed_by_file(self, session: Session, shop_id: int, file: ByteString):
        file = pd.read_excel(file)
        df = file.fillna(0)
        article_products = [i for i in df[df.columns[5]]]
        article_rf = [i for i in df[df.columns[0]]]
        price_rf_kg = [i for i in df[df.columns[4]]]
        price_rf = [i for i in df[df.columns[3]]]
        data_file = zip(article_products, article_rf, price_rf_kg, price_rf)
        with session as db:
            for data in data_file:
                data_object = self.model(
                    product_article=data[0], article_rf=data[1], price_rf_kg=data[2],
                    price_rf=data[3], shop_id=shop_id
                )
                db.add(data_object)
            db.commit()
        self.create_processed_analyse(session, shop_id)
        return {'status': 'Ok'}

    def create_processed_analyse(self, session: Session, shop_id: int):
        with session as db:
            processed_products = db.query(self.model).filter(self.model.shop_id == shop_id).all()
            for processed_product in processed_products:
                product = db.query(Product).filter(
                    Product.shop_id == shop_id,
                    Product.article == processed_product.product_article
                ).first()
                if product:
                    analise_object = self.analise_model(
                        name=product.name, price_rf=processed_product.price_rf,
                        price_rf_kg=processed_product.price_rf_kg, product_price=product.price,
                        sale_price=product.sale_price, weight=product.weight, unit=product.unit,
                        product_article=product.article, article_rf=processed_product.article_rf,
                        shop_id=shop_id
                    )
                    db.add(analise_object)
            db.commit()


class CRUDProcessedAnalise(CRUDBase):
    model = ProcessedAnalise

    def get_analise_by_shop_id(self, session: Session, shop_id: int):
        with session as db:
            analise_products = db.query(self.model).filter(self.model.shop_id == shop_id).all()
            if not analise_products:
                raise HTTPException(status_code=404, detail=f'analise product not found by shop_id: {shop_id}')
            return analise_products

    def get_analise_file_by_shop_id(self, shop_id: int):
        statement = select(self.model).where(self.model.shop_id == shop_id)
        df = pd.read_sql(statement, legacy_engine)
        return df














