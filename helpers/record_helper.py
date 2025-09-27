from typing import List

from bson import ObjectId

from helpers.attempt_helper import attempt_helper


async def record_helper(record: dict, attempt_collection) -> dict:
    attempts: List[dict] = []
    for attempt_id in record.get("attempts", []):
        attempt_doc = await attempt_collection.find_one({"_id": ObjectId(attempt_id)})
        if attempt_doc:
            attempts.append(attempt_helper(attempt_doc))

    return {
        "id": str(record["_id"]),
        "max_time": record["max_time"],
        "min_time": record["min_time"],
        "attempts": attempts,
        "total_errors": record["total_errors"],
        "exercise_id": record.get("exercise_id")

    }