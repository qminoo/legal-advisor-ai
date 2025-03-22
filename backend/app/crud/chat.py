from sqlalchemy.orm import Session
from ..models.chat import ChatSession, ChatMessage

async def create_chat_session(db: Session) -> ChatSession:
    db_session = ChatSession()
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

async def create_chat_message(
    db: Session,
    session_id: int,
    role: str,
    content: str
) -> ChatMessage:
    db_message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

async def get_chat_history(db: Session, session_id: int):
    return db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at.asc()).all()

async def get_all_chat_sessions(db: Session):
    sessions = db.query(ChatSession).order_by(ChatSession.created_at.desc()).all()
    response = {"sessions": [{"id": session.id, "created_at": str(session.created_at)} for session in sessions]}
    return response
 
