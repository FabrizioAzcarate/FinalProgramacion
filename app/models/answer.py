from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from datetime import datetime
from ..database import Base

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    quiz_session_id = Column(Integer, ForeignKey("quiz_sessions.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))

    respuesta_seleccionada = Column(Integer, nullable=False)
    es_correcta = Column(Boolean, nullable=False)
    tiempo_respuesta_segundos = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
