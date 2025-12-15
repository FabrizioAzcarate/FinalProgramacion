from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.quiz_session import QuizSession
from ..schemas.quiz_session import QuizSessionCreate, QuizSessionResponse
from ..services.quiz_service import QuizService

router = APIRouter()


@router.post("/", response_model=QuizSessionResponse)
def iniciar_sesion(payload: QuizSessionCreate, db: Session = Depends(get_db)):
    sesion = QuizSession(
        usuario_nombre=payload.usuario_nombre,
        estado="en_progreso"
    )
    db.add(sesion)
    db.commit()
    db.refresh(sesion)
    return sesion


@router.get("/", response_model=list[QuizSessionResponse])
def listar_sesiones(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(QuizSession).offset(skip).limit(limit).all()


@router.get("/{session_id}", response_model=QuizSessionResponse)
def obtener_sesion(session_id: int, db: Session = Depends(get_db)):
    sesion = db.query(QuizSession).filter(QuizSession.id == session_id).first()
    if not sesion:
        raise HTTPException(404, "Sesión no encontrada")
    return sesion


@router.put("/{session_id}/complete", response_model=QuizSessionResponse)
def completar_sesion(session_id: int, db: Session = Depends(get_db)):
    sesion = db.query(QuizSession).filter(QuizSession.id == session_id).first()
    if not sesion:
        raise HTTPException(404, "Sesión no encontrada")

    if sesion.estado != "en_progreso":
        raise HTTPException(400, "La sesión ya fue completada o abandonada")

    return QuizService.finalizar_sesion(db, sesion)


@router.delete("/{session_id}")
def eliminar_sesion(session_id: int, db: Session = Depends(get_db)):
    sesion = db.query(QuizSession).filter(QuizSession.id == session_id).first()
    if not sesion:
        raise HTTPException(404, "Sesión no encontrada")
    db.delete(sesion)
    db.commit()
    return {"message": "Sesión eliminada correctamente"}
