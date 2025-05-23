from fastapi import APIRouter
from fastapi import HTTPException
from services.chatbot import get_answer
from api.models import AnswerResponse
from api.models import AskRequest

router = APIRouter()


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(req: AskRequest):
    try:
        answer = get_answer(req.question)
        return AnswerResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
