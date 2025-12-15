from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.quiz_service import QuizService

router = APIRouter()


@router.get("/global")
def estadisticas_globales(db: Session = Depends(get_db)):
    return QuizService.estadisticas_globales(db)


@router.get("/session/{session_id}")
def estadisticas_sesion(session_id: int, db: Session = Depends(get_db)):
    result = QuizService.estadisticas_sesion(db, session_id)
    if not result:
        raise HTTPException(404, "Sesión no encontrada")
    return result


@router.get("/questions/difficult")
def preguntas_dificiles(db: Session = Depends(get_db)):
    return QuizService.preguntas_dificiles(db)


@router.get("/categories")
def categorias(db: Session = Depends(get_db)):
    return QuizService.estadisticas_por_categoria(db)
