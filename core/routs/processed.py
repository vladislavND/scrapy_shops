import io
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlmodel import Session
from starlette.responses import StreamingResponse

from core.models.processeed import ProcessedAnalise
from core.db.dependecy import get_db
from core.crud.processed import CRUDProcessed, CRUDProcessedAnalise
from core.schema import ResponseModel


router = APIRouter()
crud = CRUDProcessed()
crud_analise = CRUDProcessedAnalise()


@router.post('/add_processed_by_file', response_model=ResponseModel)
async def add_processed_by_file(
        shop_id: int,
        file: UploadFile = File(
        'test.xlsx',
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ), session: Session = Depends(get_db)):
    file = await file.read()

    return crud.add_processed_by_file(file=file, shop_id=shop_id, session=session)


@router.get('/get_all_analise_products', response_model=List[ProcessedAnalise])
def get_all_processed_products(session: Session = Depends(get_db)):
    return crud_analise.get_all(session)


@router.get('/get_analise_product/{pk}', response_model=ProcessedAnalise)
def get_analise_product(pk: int, session: Session = Depends(get_db)):
    return crud_analise.get(session, pk)


@router.get('/get_analise_by/{shop_id}', response_model=List[ProcessedAnalise])
def get_analise_by_shop_id(shop_id: int, session: Session = Depends(get_db)):
    return crud_analise.get_analise_by_shop_id(session, shop_id)


@router.get('/get_analise_file_by/{shop_id}', response_class=StreamingResponse)
def get_analise_file_by_shop_id(shop_id: int):
    df = crud_analise.get_analise_file_by_shop_id(shop_id)
    to_write = io.BytesIO()
    df.to_excel(to_write, index=False)
    to_write.seek(0)
    return StreamingResponse(to_write, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')





