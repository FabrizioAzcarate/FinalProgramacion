from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from .database import Base, engine
from .routers import questions, quiz_sessions, statistics, answer

# Crear Tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Quiz API",
    description="API para gestionar preguntas, sesiones y estadísticas de un quiz",
    version="1.0.0"
)

# Registrar Routers
app.include_router(questions, prefix="/questions", tags=["Questions"])
app.include_router(quiz_sessions, prefix="/quiz-sessions", tags=["Quiz Sessions"])
app.include_router(statistics, prefix="/statistics", tags=["Statistics"])
app.include_router(answer, prefix="/answers", tags=["Answers"])

@app.get("/")
def root():
    return {"message": "API Quiz funcionando"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)


@app.get("/docs/session/{session_id}", include_in_schema=False)
def docs_session_redirect(session_id: int):
    return RedirectResponse(url=f"/quiz-sessions/{session_id}")
