
from typing import List

from sqlmodel import Session, select


from core.crud.base import CRUDBase
from core.models.price import Price


class CRUDPrice(CRUDBase):
    model = Price

    def get_price_by_article(self, session: Session, article: int) -> List[Price]:
        price = session.exec(select(self.model).filter_by(article=article)).all()
        return price
