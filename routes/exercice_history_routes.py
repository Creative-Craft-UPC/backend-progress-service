from typing import List
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse

from schemas.exercice_history_schema import ExerciceHistoryResponse, ExerciceHistorySchema
from database.database import attempts_collection, exercice_histories_collection
from helpers.exercice_history_helper import exercice_history_helper

router = APIRouter()

# POST
@router.post("/", response_model=ExerciceHistoryResponse, status_code=status.HTTP_201_CREATED)
async def create_exercice_history(exerciceHistory: ExerciceHistorySchema):
    
    result = await exercice_histories_collection.insert_one(exerciceHistory.dict())
    saved_exercice_history = await exercice_histories_collection.find_one({"_id": result.inserted_id})
    return await exercice_history_helper(saved_exercice_history, attempts_collection)

#GET
@router.get("/", response_model=List[ExerciceHistoryResponse], status_code=201)
async def get_exercice_historties():
    exercice_histories = []
    async for exercice_history in exercice_histories_collection.find():
        exercice_histories.append(await exercice_history_helper(exercice_history, attempts_collection))
    return exercice_histories

#GET
@router.get("/{exercice_history_id}", response_model=ExerciceHistoryResponse, status_code=201)
async def get_exercice_history_by_id(exercice_history_id: str = Path(..., description="Exercice history Id")):
    if not ObjectId(exercice_history_id):
        raise HTTPException(status_code=400, detail="Id invalido")
    exercice_history = await exercice_histories_collection.find_one({"_id": ObjectId(exercice_history_id)})
    if exercice_history:
        return await exercice_history_helper(exercice_history, attempts_collection)
    raise HTTPException(status_code=404, detail="Registro no encontrado")

#PATCH
@router.patch("/{exercice_history_id}", response_model=ExerciceHistoryResponse, status_code=201)
async def patch_exercice_history(exercice_history_id: str, exercice_history: ExerciceHistorySchema):
    if not ObjectId(exercice_history_id):
        raise HTTPException(status_code=400, detail="Id invalido")
    updated_exercice_history = await exercice_histories_collection.find_one_and_update({"_id": ObjectId(exercice_history_id)}, {"$set": exercice_history.dict()})

    if updated_exercice_history:
        return await exercice_history_helper(exercice_history, attempts_collection)
    raise HTTPException(status_code=404, detail="Registro no encontrado")
    

#DELETE
@router.delete("/{exercice_history_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercice_history(exercice_history_id: str):
    if not ObjectId(exercice_history_id):
        raise HTTPException(status_code=400, detail="Id invalido")
    exercice_history = await exercice_histories_collection.find_one({"_id": ObjectId(exercice_history_id)})
    if not exercice_history:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    attempts_id = exercice_history.get("attempts",[])
    if attempts_id:
        await attempts_collection.delete_many({"_id": {"$in": attempts_id}})
    
    result = await exercice_histories_collection.delete_one({"_id": ObjectId(exercice_history_id)})
    if result.deleted_count == 0:
         raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

