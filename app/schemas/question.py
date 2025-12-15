from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
import unicodedata


# Categorias y Dificultades Permitidas
ALLOWED_CATEGORIES = [
    "tecnologia",
    "historia",
    "ciencia",
    "general",
    "math",
    "science",
    "history",
    "geografia",
    "arte",
]
ALLOWED_DIFFICULTIES = [
    "facil",
    "medio",
    "dificil",
    "easy",
    "medium",
    "hard",
]


def _normalize_text(s: str) -> str:
    if s is None:
        return ""
    s = str(s)
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


# Base
class QuestionBase(BaseModel):
    pregunta: str
    opciones: List[str]
    respuesta_correcta: int
    categoria: str
    dificultad: str
    explicacion: Optional[str] = None


# Creacion
class QuestionCreate(QuestionBase):

    @field_validator("respuesta_correcta", mode="after")
    @classmethod
    def validar_respuesta(cls, v, info):
        opciones = info.data.get("opciones", [])
        if v < 0 or v >= len(opciones):
            raise ValueError("respuesta_correcta fuera del rango de opciones")
        return v

    @field_validator("opciones")
    @classmethod
    def validar_opciones(cls, v):
        if not (3 <= len(v) <= 5):
            raise ValueError("'opciones' debe contener entre 3 y 5 elementos")
        return v

    @field_validator("categoria")
    @classmethod
    def validar_categoria(cls, v):
        if _normalize_text(v) not in { _normalize_text(x) for x in ALLOWED_CATEGORIES }:
            raise ValueError(f"categoria inválida. Debe ser una de: {ALLOWED_CATEGORIES}")
        return v

    @field_validator("dificultad")
    @classmethod
    def validar_dificultad(cls, v):
        if _normalize_text(v) not in { _normalize_text(x) for x in ALLOWED_DIFFICULTIES }:
            raise ValueError(f"dificultad inválida. Debe ser una de: {ALLOWED_DIFFICULTIES}")
        return v


# Actualizacion
class QuestionUpdate(BaseModel):
    pregunta: Optional[str] = None
    opciones: Optional[List[str]] = None
    respuesta_correcta: Optional[int] = None
    categoria: Optional[str] = None
    dificultad: Optional[str] = None
    explicacion: Optional[str] = None
    is_active: Optional[bool] = None


# Respuestas
class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime
    is_active: bool

    model_config = {"from_attributes": True}
