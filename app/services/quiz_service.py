from sqlalchemy.orm import Session
from ..models.answer import Answer
from ..models.question import Question
from ..models.quiz_session import QuizSession
from datetime import datetime


class QuizService:

    # Calculo de Sesion Completa
    @staticmethod
    def finalizar_sesion(db: Session, session: QuizSession):
        respuestas = db.query(Answer).filter(Answer.quiz_session_id == session.id).all()

        total_preguntas = len(respuestas)
        correctas = sum(1 for r in respuestas if r.es_correcta)

        session.preguntas_respondidas = total_preguntas
        session.preguntas_correctas = correctas
        session.puntuacion_total = correctas * 10

        session.fecha_fin = datetime.utcnow()

        # Duración Total
        if session.fecha_inicio and session.fecha_fin:
            session.tiempo_total_segundos = int((session.fecha_fin - session.fecha_inicio).total_seconds())

        session.estado = "completado"

        db.commit()
        db.refresh(session)

        return session

    # Estadisticas (Globales)
    @staticmethod
    def estadisticas_globales(db: Session):
        total_preguntas = db.query(Question).filter(Question.is_active == True).count()

        sesiones = db.query(QuizSession).filter(QuizSession.estado == "completado").all()
        total_sesiones = len(sesiones)

        if total_sesiones > 0:
            promedio_aciertos = sum(s.preguntas_correctas for s in sesiones) / total_sesiones
        else:
            promedio_aciertos = 0

        # Categorias dificiles
        preguntas = db.query(Question).all()
        categoria_stats = {}

        for p in preguntas:
            respuestas = db.query(Answer).filter(Answer.question_id == p.id).all()
            if len(respuestas) == 0:
                continue
            incorrectas = sum(1 for r in respuestas if not r.es_correcta)
            tasa_error = incorrectas / len(respuestas)

            if p.categoria not in categoria_stats:
                categoria_stats[p.categoria] = []
            categoria_stats[p.categoria].append(tasa_error)

        categorias_dificiles = {
            cat: sum(vals) / len(vals)
            for cat, vals in categoria_stats.items()
        }

        return {
            "total_preguntas_activas": total_preguntas,
            "total_sesiones_completadas": total_sesiones,
            "promedio_aciertos_general": promedio_aciertos,
            "categorias_mas_dificiles": categorias_dificiles,
        }

    # Estadisticas (por Sesion)
    @staticmethod
    def estadisticas_sesion(db: Session, session_id: int):
        session = db.query(QuizSession).filter(QuizSession.id == session_id).first()
        if not session:
            return None

        respuestas = db.query(Answer).filter(Answer.quiz_session_id == session_id).all()

        if len(respuestas) > 0:
            tiempo_promedio = sum(
                r.tiempo_respuesta_segundos for r in respuestas if r.tiempo_respuesta_segundos
            ) / len(respuestas)
        else:
            tiempo_promedio = 0

        detalle = []
        for r in respuestas:
            pregunta = db.query(Question).filter(Question.id == r.question_id).first()
            detalle.append({
                "pregunta": pregunta.pregunta,
                "opciones": pregunta.opciones,
                "respuesta_correcta": pregunta.respuesta_correcta,
                "respuesta_usuario": r.respuesta_seleccionada,
                "es_correcta": r.es_correcta
            })

        return {
            "puntuacion_final": session.puntuacion_total,
            "porcentaje_aciertos": (session.preguntas_correctas / session.preguntas_respondidas * 100)
                                    if session.preguntas_respondidas > 0 else 0,
            "tiempo_promedio_por_pregunta": tiempo_promedio,
            "respuestas": detalle
        }

    # Preguntas mas Dificiles
    @staticmethod
    def preguntas_dificiles(db: Session):
        preguntas = db.query(Question).all()
        resultado = []

        for p in preguntas:
            respuestas = db.query(Answer).filter(Answer.question_id == p.id).all()
            if not respuestas:
                continue

            incorrectas = sum(1 for r in respuestas if not r.es_correcta)
            total = len(respuestas)
            tasa_error = incorrectas / total

            resultado.append({
                "pregunta": p.pregunta,
                "veces_respondida": total,
                "incorrectas": incorrectas,
                "tasa_de_error": tasa_error
            })

        # Orden por Mayor Dificultad
        resultado.sort(key=lambda x: x["tasa_de_error"], reverse=True)
        return resultado

    # Estadisticas (por Categoria)
    @staticmethod
    def estadisticas_por_categoria(db: Session):
        preguntas = db.query(Question).all()
        categorias = {}

        for q in preguntas:
            if q.categoria not in categorias:
                categorias[q.categoria] = {"preguntas": 0, "correctas": 0, "total": 0}

            categorias[q.categoria]["preguntas"] += 1

            respuestas = db.query(Answer).filter(Answer.question_id == q.id).all()

            for r in respuestas:
                categorias[q.categoria]["total"] += 1
                if r.es_correcta:
                    categorias[q.categoria]["correctas"] += 1

        # Resultado Final
        resultado = {}
        for cat, data in categorias.items():
            if data["total"] > 0:
                resultado[cat] = data["correctas"] / data["total"]
            else:
                resultado[cat] = None
        return resultado
