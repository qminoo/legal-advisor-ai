from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..chains.legal_advisor import LegalAdvisorChain

router = APIRouter(tags=["chat"])

legal_advisor = LegalAdvisorChain()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = await legal_advisor.get_response(request.question)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 