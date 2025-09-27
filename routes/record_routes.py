from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse

from schemas.record_schema import RecordResponse, RecordSchema
from database.database import attempts_collection, records_collection
from helpers.record_helper import record_helper

router = APIRouter()

# POST
@router.post("/", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
async def create_record(Record: RecordSchema):
    
    result = await records_collection.insert_one(Record.dict())
    saved_record = await records_collection.find_one({"_id": result.inserted_id})
    return await record_helper(saved_record, attempts_collection)

#GET
@router.get("/", response_model=List[RecordResponse], status_code=201)
async def get_records():
    records = []
    async for record in records_collection.find():
        records.append(await record_helper(record, attempts_collection))
    return records

#GET
@router.get("/{record_id}", response_model=RecordResponse, status_code=201)
async def get_record_by_id(record_id: str = Path(..., description="Records Id")):
    if not ObjectId(record_id):
        raise HTTPException(status_code=400, detail="Id invalido")
    record = await records_collection.find_one({"_id": ObjectId(record_id)})
    if record:
        return await record_helper(record, attempts_collection)
    raise HTTPException(status_code=404, detail="Registro no encontrado")

#PATCH
@router.patch("/{record_id}", response_model=RecordResponse, status_code=201)
async def patch_record(record_id: str, record: RecordSchema):
    if not ObjectId(record_id):
        raise HTTPException(status_code=400, detail="Id invalido")
    updated_record = await records_collection.find_one_and_update({"_id": ObjectId(record_id)}, {"$set": record.dict()})

    if updated_record:
        return await record_helper(record, attempts_collection)
    raise HTTPException(status_code=404, detail="Registro no encontrado")
    

#DELETE
@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(record_id: str):
    if not ObjectId(record_id):
        raise HTTPException(status_code=400, detail="Id invalido")
    record = await records_collection.find_one({"_id": ObjectId(record_id)})
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    attempts_id = record.get("attempts",[])
    if attempts_id:
        await attempts_collection.delete_many({"_id": {"$in": attempts_id}})
    
    result = await records_collection.delete_one({"_id": ObjectId(record_id)})
    if result.deleted_count == 0:
         raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

