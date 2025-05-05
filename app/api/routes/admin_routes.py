from fastapi import APIRouter, HTTPException

from app.config.database import MongoDB

admin_bp = APIRouter()

@admin_bp.get("/stats")
async def get_statistics():
    db = MongoDB.get_db()
    try:
        user_count = db["users"].count_documents({})
        conversation_count = db["conversations"].count_documents({})
        message_count = db["messages"].count_documents({})

        return {
            "users": user_count,
            "conversations": conversation_count,
            "messages": message_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

