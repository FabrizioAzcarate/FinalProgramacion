from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.answer import Answer
from ..models.question import Question
from ..models.quiz_session import QuizSession
from ..schemas.answer import AnswerCreate, AnswerResponse

router = APIRouter()


@router.post("/", response_model=AnswerResponse)
def registrar_respuesta(payload: AnswerCreate, db: Session = Depends(get_db)):
    # validar sesión
    sesion = db.query(QuizSession).filter(QuizSession.id == payload.quiz_session_id).first()
    if not sesion:
        raise HTTPException(404, "Sesión no existe")

    # validar pregunta
    pregunta = db.query(Question).filter(Question.id == payload.question_id).first()
    if not pregunta:
        raise HTTPException(404, "Pregunta no existe")

    # evitar responder dos veces la misma pregunta
    existente = db.query(Answer).filter(
        Answer.quiz_session_id == payload.quiz_session_id,
        Answer.question_id == payload.question_id
    ).first()

    if existente:
        raise HTTPException(400, "La pregunta ya fue respondida en esta sesión")

    # validar rango
    if payload.respuesta_seleccionada < 0 or payload.respuesta_seleccionada >= len(pregunta.opciones):
        raise HTTPException(400, "La respuesta está fuera de rango")

    es_correcta = payload.respuesta_seleccionada == pregunta.respuesta_correcta

    respuesta = Answer(
        quiz_session_id=payload.quiz_session_id,
        question_id=payload.question_id,
        respuesta_seleccionada=payload.respuesta_seleccionada,
        tiempo_respuesta_segundos=payload.tiempo_respuesta_segundos,
        es_correcta=es_correcta
    )

    db.add(respuesta)
    db.commit()
    db.refresh(respuesta)

    return respuesta


@router.get("/session/{session_id}", response_model=list[AnswerResponse])
def respuestas_por_sesion(session_id: int, db: Session = Depends(get_db)):
    return db.query(Answer).filter(Answer.quiz_session_id == session_id).all()


@router.get("/{answer_id}", response_model=AnswerResponse)
def obtener_respuesta(answer_id: int, db: Session = Depends(get_db)):
    r = db.query(Answer).filter(Answer.id == answer_id).first()
    if not r:
        raise HTTPException(404, "Respuesta no encontrada")
    return r


@router.put("/{answer_id}", response_model=AnswerResponse)
def actualizar_respuesta(answer_id: int, payload: AnswerCreate, db: Session = Depends(get_db)):
    r = db.query(Answer).filter(Answer.id == answer_id).first()
    if not r:
        raise HTTPException(404, "Respuesta no encontrada")

    pregunta = db.query(Question).filter(Question.id == payload.question_id).first()
    if not pregunta:
        raise HTTPException(404, "Pregunta no existe")

    r.respuesta_seleccionada = payload.respuesta_seleccionada
    r.es_correcta = payload.respuesta_seleccionada == pregunta.respuesta_correcta
    r.tiempo_respuesta_segundos = payload.tiempo_respuesta_segundos

    db.commit()
    db.refresh(r)
    return r
