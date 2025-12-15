from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.types import JSON
from datetime import datetime
from ..database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    pregunta = Column(String, nullable=False)
    opciones = Column(JSON, nullable=False)
    respuesta_correcta = Column(Integer, nullable=False)
    explicacion = Column(Text, nullable=True)
    categoria = Column(String, nullable=False)
    dificultad = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
