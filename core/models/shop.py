from typing import List, Optional

from sqlmodel import SQLModel, Relationship, Field


class FileBase(SQLModel):
    file_name: str
    path: str

    shop_id: Optional[int] = Field(default=None, foreign_key="shop.id")
    team: Optional['Shop'] = Relationship(back_populates="files")


class File(FileBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ShopBase(SQLModel):
    name: str
    url: str
    file: List[File] = Relationship(back_populates='shops')


class Shop(ShopBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


