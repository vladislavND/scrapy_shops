import json
from typing import List
import os

import pandas as pd
from pydantic import parse_obj_as
from fastapi import HTTPException

from core.crud.base import CRUDBase
from core.crud.shop import CRUDShop
from core.models.product import Product, ProductBase
from core.db.database import Session


class CRUDProduct(CRUDBase):
    model = Product

    def add_product_by_file(self, session: Session, shop_id: int, file_name: str):
        try:
            df = pd.read_csv(f'parse_files/{file_name}', sep=';', encoding='utf-8', low_memory=False, index_col=False)
            df['shop_id'] = shop_id
            df1 = df[['article', 'price', 'sale_price', 'shop_id', 'weight', 'unit', 'name']]
            json_data = df1.to_json(index=False, orient='table')
            data = json.loads(json_data)['data']
            objects = parse_obj_as(List[ProductBase], data)
            with session as db:
                for product in objects:
                    product_object = self.model.from_orm(product)
                    db.add(product_object)
                db.commit()
            return {'status': 'Ok'}
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Не удалось создать продукты из файла: {file_name}")

    def get_products_by_shop_id(self, session: Session, shop_id) -> List[Product]:
        with session as db:
            objects = db.query(self.model).filter(self.model.shop_id == shop_id).all()
            return objects

    def get_file_names_by_shop_id(self, session: Session, shop_id: int):
        print(type(shop_id))
        print(shop_id)
        shop_crud = CRUDShop()
        shop_name = shop_crud.get(session, shop_id).name
        directory_files = os.listdir('parse_files')
        files = []

        for file in directory_files:
            if shop_name in file:
                files.append(file)

        if not files:
            raise HTTPException(status_code=404, detail=f'Files not found by shop_id: {shop_id}')

        return files

    def get_file_by_name(self, name: str) -> pd.DataFrame:
        df = pd.read_csv(f'parse_files/{name}', sep=';', encoding='utf-8', low_memory=False, index_col=False)
        return df










