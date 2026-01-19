from pydantic import BaseModel
from typing import Optional, Literal, Union

# --- API Responses Data Models ---
class BaseResponseData(BaseModel):
    session_id: str
    assessment_done: bool
    confidence: float

class AskResponseData(BaseResponseData):
    response_type: Literal["question"] = "question"
    content: str

class AnswerResponseData(BaseResponseData):
    response_type: Literal["answer"] = "answer"
    content: str
    explanation: str
    disclaimer: str
    confidence_level: Literal["high", "medium", "low"]

# --- Generic API Response Wrappers ---
class APIResponse(BaseModel):
    statusCode: int
    message: str
    success: bool
    data: Optional[Union[AskResponseData, AnswerResponseData]] = None

class AskResponse(APIResponse):
    data: AskResponseData

class AnswerResponse(APIResponse):
    data: AnswerResponseData
