def attempt_helper(attempt: dict) -> dict:
    return {
        "id": str(attempt["_id"]),
        "time": attempt["time"],
        "errors_quantity": attempt["errors_quantity"],
    }