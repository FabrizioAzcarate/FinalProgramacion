from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuizSessionCreate(BaseModel):
    usuario_nombre: Optional[str] = None


class QuizSessionResponse(BaseModel):
    id: int
    usuario_nombre: Optional[str]
    fecha_inicio: datetime
    fecha_fin: Optional[datetime]
    puntuacion_total: int
    preguntas_respondidas: int
    preguntas_correctas: int
    estado: str
    tiempo_total_segundos: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}
