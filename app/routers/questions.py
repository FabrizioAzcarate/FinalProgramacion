from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import random
import unicodedata

from app.database import get_db
from app.models.question import Question
from app.schemas.question import (
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
    ALLOWED_CATEGORIES,
    ALLOWED_DIFFICULTIES,
)

router = APIRouter()

def _normalize_text(s: str) -> str:
    if s is None:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(s))
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()

# Crear Pregunta
@router.post("/", response_model=QuestionResponse)
def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db)
):
    db_question = Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


# Crear Preguntas en Bulk
@router.post("/bulk", response_model=List[QuestionResponse])
def bulk_create(
    questions: List[QuestionCreate],
    db: Session = Depends(get_db)
):
    objs: List[Question] = []

    for i, qc in enumerate(questions):
        try:
            objs.append(Question(**qc.model_dump()))
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"Error en la pregunta {i}: {str(e)}"
            )

    try:
        db.add_all(objs)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar preguntas: {str(e)}"
        )

    for o in objs:
        db.refresh(o)
    return objs

# Listar las Preguntas
@router.get("/", response_model=List[QuestionResponse])
def list_questions(
    categoria: Optional[str] = None,
    dificultad: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Question).filter(Question.is_active == True)

    if categoria:
        query = query.filter(Question.categoria == categoria)

    if dificultad:
        query = query.filter(Question.dificultad == dificultad)

    return query.offset(skip).limit(limit).all()

# Preguntas Aleatorias
@router.get("/random", response_model=List[QuestionResponse])
def random_questions(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    items = db.query(Question).filter(Question.is_active == True).all()

    if not items:
        return []

    limit = min(limit, len(items))
    return random.sample(items, limit)

# Obtener una Pregunta por ID
@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    return q

# Actualizar Pregunta
@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    payload: QuestionUpdate,
    db: Session = Depends(get_db)
):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    if payload.pregunta is not None:
        q.pregunta = payload.pregunta

    if payload.opciones is not None:
        if not (3 <= len(payload.opciones) <= 5):
            raise HTTPException(
                status_code=400,
                detail="'opciones' debe tener entre 3 y 5 elementos"
            )
        q.opciones = payload.opciones

    if payload.respuesta_correcta is not None:
        opciones_len = len(payload.opciones) if payload.opciones else len(q.opciones)
        if payload.respuesta_correcta < 0 or payload.respuesta_correcta >= opciones_len:
            raise HTTPException(
                status_code=400,
                detail="respuesta_correcta fuera del rango"
            )
        q.respuesta_correcta = payload.respuesta_correcta

    if payload.categoria is not None:
        if _normalize_text(payload.categoria) not in {
            _normalize_text(x) for x in ALLOWED_CATEGORIES
        }:
            raise HTTPException(
                status_code=400,
                detail=f"Categoria inválida. Debe ser una de {ALLOWED_CATEGORIES}"
            )
        q.categoria = payload.categoria

    if payload.dificultad is not None:
        if _normalize_text(payload.dificultad) not in {
            _normalize_text(x) for x in ALLOWED_DIFFICULTIES
        }:
            raise HTTPException(
                status_code=400,
                detail=f"Dificultad inválida. Debe ser una de {ALLOWED_DIFFICULTIES}"
            )
        q.dificultad = payload.dificultad

    if payload.explicacion is not None:
        q.explicacion = payload.explicacion

    if payload.is_active is not None:
        q.is_active = payload.is_active

    db.commit()
    db.refresh(q)
    return q

# Borrado de Pregunta
@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    q.is_active = False
    db.commit()
    db.refresh(q)

    return {"message": "Pregunta desactivada correctamente"}
