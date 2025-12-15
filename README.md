# Trabajo Final de Programacion
### Por Fabrizio Azcarate

API REST desarrollada con **FastAPI** para gestionar preguntas, sesiones de quiz y respuestas, con validaciones automáticas y documentación interactiva por medio de Swagger.

## Medios Utilizados
* Python
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite
* Uvicorn

### Requisitos:
* Python 3.10 o superior
* Git (opcional)

### Instalación (Windows)
# Clonar el repositorio:
"git clone https://github.com/FabrizioAzcarate/FinalProgramacion.git"
"cd quiz-api"

# Crear el Entorno Virtual:
"python -m venv venv"
"venv\Scripts\activate"

# Instalar las Dependencias:
pip install -r requirements.txt

### Instalación (Linux)
# Clonar el repositorio
"git clone https://github.com/tu-usuario/quiz-api.git"
"cd quiz-api"

# Crear el Entorno Virtual:
"python3 -m venv venv"
"source venv/bin/activate"

# Instalar las Dependencias:
"pip install -r requirements.txt"

## Configuración del Trabajo
Por defecto el proyecto usa **SQLite**, por lo que no requiere configuración adicional.

Para iniciar el servidor:
(En la Terminal de Visual Studio Code)
"uvicorn app.main:app --reload"

La API va a estar disponible en:
* http://127.0.0.1:8000
* Swagger UI: http://127.0.0.1:8000/docs
