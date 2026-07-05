from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from app.models.schemas import UserQueryRequest
from app.api.responses import AskResponse, AnswerResponse, EscalationResponse, AskResponseData, AnswerResponseData, EscalationResponseData, APIResponse
from app.services.orchestrator import Orchestrator
from app.api import deps
from app.api.auth import router as auth_router
from app.api.sessions import router as sessions_router
from app.api.contact import router as contact_router
from app.api.chat_sessions import router as chat_sessions_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth")
router.include_router(sessions_router, prefix="/auth/sessions")
router.include_router(contact_router, prefix="/contact")
router.include_router(chat_sessions_router, prefix="/chat")

@router.post("/query", response_model=APIResponse)
async def query_endpoint(
    request: UserQueryRequest,
    current_user: dict = Depends(deps.get_current_user),
    orchestrator: Orchestrator = Depends(deps.get_orchestrator)
):
    try:
        result = await orchestrator.handle_query(
            request.session_id, request.message, current_user["user_id"]
        )
        
        if isinstance(result, AskResponseData):
            msg = "Question computed successfully"
        elif isinstance(result, EscalationResponseData):
            msg = "Session escalated to doctor"
        else:
            msg = "Answer generated successfully"
        
        return APIResponse(
            statusCode=200,
            message=msg,
            success=True,
            data=result
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
