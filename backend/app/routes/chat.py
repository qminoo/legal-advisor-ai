from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..crud.chat import create_chat_session, create_chat_message, get_all_chat_sessions, get_chat_history
from ..chains.legal_advisor import LegalAdvisorChain
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(
    chat_request: ChatRequest,
    session_id: int = None,
    db: Session = Depends(get_db)
):
    try:
        if not session_id:
            chat_session = await create_chat_session(db)
            session_id = chat_session.id
            created_at = chat_session.created_at

        await create_chat_message(db, session_id, "user", chat_request.message)

        legal_chain = LegalAdvisorChain()
        response = await legal_chain.get_response(chat_request.message)

        await create_chat_message(db, session_id, "assistant", response)

        return {
            "session_id": session_id,
            "created_at": str(created_at),
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat-history/{session_id}")
async def get_session_history(
    session_id: int,
    db: Session = Depends(get_db)
):
    messages = await get_chat_history(db, session_id)
    return {"messages": messages} 

@router.get("/all-sessions")
async def get_all_sessions(
    db: Session = Depends(get_db)
):
    sessions = await get_all_chat_sessions(db)
    return sessions