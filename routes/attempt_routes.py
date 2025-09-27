from datetime import datetime
from fastapi import APIRouter, HTTPException, Path, status
from typing import List

from fastapi.responses import JSONResponse
from schemas.attempt_schema import AttemptDto, AttemptResponse, AttemptSchema
from helpers.attempt_helper import attempt_helper
from database.database import attempts_collection, records_collection
from bson import ObjectId


# Simulación de base de datos en memoria
router = APIRouter()

#POST
@router.post("/{record_id}", response_model=AttemptResponse, status_code=status.HTTP_201_CREATED)
async def create_attempt(attempt: AttemptDto, record_id: str = Path(..., description="Record Id")):

    if not ObjectId.is_valid(record_id):
        raise HTTPException(status_code=400, detail="ID del registro inválido")

    record = await records_collection.find_one({"_id": ObjectId(record_id)})
    if not record:
         raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    # construir schema automáticamente
    attempt_object = AttemptSchema(
        time=attempt.time,
        errors_quantity=attempt.errors_quantity,
        date=datetime.utcnow().isoformat()
    )

    result = await attempts_collection.insert_one(attempt_object.dict())

    #Calcular min_time:
    prev_min = record.get("min_time")
    if prev_min is None or prev_min == 0:
        new_min = attempt.time
    else:
        new_min = min(attempt.time, prev_min)

    await records_collection.update_one(
        {"_id": ObjectId(record_id)},
        {"$push": {"attempts": result.inserted_id},
         "$inc": {"total_errors": attempt.errors_quantity},
         "$set": {
            "max_time": max(attempt.time, record.get("max_time", attempt.time)),
            "min_time": new_min,
         }}
    )

    saved_attempt = await attempts_collection.find_one({"_id": result.inserted_id})
    return attempt_helper(saved_attempt)



#GET
@router.get("/", response_model=List[AttemptResponse])
async def get_attempts():
    attempts = []
    async for attempt in attempts_collection.find():
        attempts.append(attempt_helper(attempt))
    return attempts

#GET BY RECORD ID
@router.get("/{record_id}", response_model=List[AttemptResponse])
async def get_attempt_by_id(record_id: str = Path(..., description="Record Id")):
    if not ObjectId.is_valid(record_id):
        raise HTTPException(status_code=400, detail="ID del registro inválido")

    record = await records_collection.find_one({"_id": ObjectId(record_id)})
    if not record:
         raise HTTPException(status_code=404, detail="Registro no encontrado")
    attempts = []
    for attempt_id in record.get("attempts", []):
        attempt = await attempts_collection.find_one({"_id": ObjectId(attempt_id)})
        if attempt:
            attempts.append(attempt_helper(attempt))
    return attempts


#DELETE
@router.delete("/{attempt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attempt(attempt_id: str):
    if not ObjectId.is_valid(attempt_id):
        raise HTTPException(status_code=400, detail="ID del registro inválido")
    attempt = await attempts_collection.find_one({"_id": ObjectId(attempt_id)})
    record = await records_collection.find_one({"attempts": ObjectId(attempt_id)})
    

    if(len(record.get("attempts", [])) > 1):
        #Calcular min_time:
        prev_min = record.get("min_time")
        prev_max = record.get("max_time")
        new_min = 0
        new_max = 0
        if(prev_min == attempt.get("time") or prev_max == attempt.get("time")):
            for other_attempts_id in record.get("attempts", []):
                if(other_attempts_id != ObjectId(attempt_id)):
                    other_attempt = await attempts_collection.find_one({"_id": ObjectId(other_attempts_id)})
                    other_attempt_time = other_attempt.get("time")
                    if(new_min == 0): 
                        new_min =  other_attempt_time
                    else:
                        new_min= min(other_attempt_time, new_min)
                    new_max= max(other_attempt_time, new_max)
            await records_collection.update_one(
                {"attempts": ObjectId(attempt_id)},
                {"$pull": {"attempts": ObjectId(attempt_id)},
                 "$inc": {"total_errors": -attempt.get("errors_quantity")},
                 "$set": {
                    "max_time": new_max,
                    "min_time": new_min,
                 }}
            )
                    
        else:
            await records_collection.update_one(
                {"attempts": ObjectId(attempt_id)},
                {"$pull": {"attempts": ObjectId(attempt_id)},
                 "$inc": {"total_errors": -attempt.get("errors_quantity")},
                 "$set": {
                    "max_time": prev_max,
                    "min_time": prev_min,
                 }}
            )
    else:
        await records_collection.update_one(
            {"attempts": ObjectId(attempt_id)},
            {"$pull": {"attempts": ObjectId(attempt_id)},
             "$set": {
                "total_errors": 0,
                "max_time": 0,
                "min_time": 0,
             }}
        )
    result = await attempts_collection.delete_one({"_id": ObjectId(attempt_id)})
    if result.deleted_count == 0:
         raise HTTPException(status_code=404, detail="Intento no encontrado")

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
    


