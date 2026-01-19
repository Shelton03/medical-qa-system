from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import UserQueryRequest
from app.api.responses import AskResponse, AnswerResponse, AskResponseData, AnswerResponseData, APIResponse
from app.services.orchestrator import Orchestrator
from app.api import deps

router = APIRouter()

@router.post("/query", response_model=APIResponse)
async def query_endpoint(
    request: UserQueryRequest,
    orchestrator: Orchestrator = Depends(deps.get_orchestrator)
):
    try:
        result = await orchestrator.handle_query(request.session_id, request.message)
        
        # Determine success message based on type
        msg = "Question generated successfully" if isinstance(result, AskResponseData) else "Answer generated successfully"
        
        return APIResponse(
            statusCode=200,
            message=msg,
            success=True,
            data=result
        )
    except Exception as e:
        # In a real app, careful not to expose internal error details
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
