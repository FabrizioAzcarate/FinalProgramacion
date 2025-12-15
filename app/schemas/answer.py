from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AnswerCreate(BaseModel):
    quiz_session_id: int
    question_id: int
    respuesta_seleccionada: int
    tiempo_respuesta_segundos: Optional[int] = None


class AnswerResponse(BaseModel):
    id: int
    quiz_session_id: int
    question_id: int
    respuesta_seleccionada: int
    es_correcta: bool
    tiempo_respuesta_segundos: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}
