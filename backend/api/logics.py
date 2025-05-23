from fastapi import APIRouter
from fastapi import HTTPException
from services.chatbot import get_answer
from api.models import AnswerResponse
from api.models import AskRequest
from services.cache import cache_answer
from services.cache import get_cached_answer

router = APIRouter()


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(req: AskRequest):
    try:
        question = req.question
        cached = get_cached_answer(question)
        if cached:
            return AnswerResponse(answer=cached)

        answer = get_answer(req.question)
        cache_answer(question=question, answer=answer)
        return AnswerResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
