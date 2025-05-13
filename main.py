from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os

# Crear la aplicación FastAPI
app = FastAPI(title="Tutorial SQL Educativo")

# Configurar templates y archivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar la base de datos SQLite
# Usamos SQLite por su simplicidad y porque no requiere un servidor separado
DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(DATABASE_URL, echo=True)  # echo=True muestra las consultas SQL en la consola

def init_db():
    """Inicializa la base de datos con una tabla de estudiantes y datos de ejemplo"""
    with engine.connect() as conn:
        # Crear tabla de estudiantes usando SQL puro para fines educativos
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS estudiantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER CHECK (edad >= 15 AND edad <= 18),
                grado TEXT
            )
        """))
        
        # Insertar datos de ejemplo si la tabla está vacía
        result = conn.execute(text("SELECT COUNT(*) FROM estudiantes"))
        if result.scalar() == 0:
            conn.execute(text("""
                INSERT INTO estudiantes (nombre, edad, grado) VALUES 
                ('Ana García', 15, 'Once'),
                ('Carlos López', 16, 'Decimo'),
                ('María Rodríguez', 17, 'Once')
            """))
        conn.commit()

# Inicializar la base de datos al arrancar
init_db()

@app.get("/")
async def home(request: Request):
    """Página principal que muestra la lista de estudiantes"""
    try:
        with engine.connect() as conn:
            # Usamos text() para crear consultas parametrizadas seguras
            result = conn.execute(text("SELECT * FROM estudiantes ORDER BY id"))
            estudiantes = result.fetchall()
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "estudiantes": estudiantes}
        )
    except SQLAlchemyError as e:
        # Manejo básico de errores de base de datos
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/estudiantes/")
async def crear_estudiante(
    nombre: str = Form(...),
    edad: int = Form(...),
    grado: str = Form(...)
):
    """Crear un nuevo estudiante usando una consulta parametrizada"""
    try:
        with engine.connect() as conn:
            # Ejemplo de consulta parametrizada usando text()
            query = text("""
                INSERT INTO estudiantes (nombre, edad, grado) 
                VALUES (:nombre, :edad, :grado)
            """)
            conn.execute(query, {
                "nombre": nombre,
                "edad": edad,
                "grado": grado
            })
            conn.commit()
        return RedirectResponse(url="/", status_code=303)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/estudiantes/{estudiante_id}/eliminar")
async def eliminar_estudiante(estudiante_id: int):
    """Eliminar un estudiante por ID usando una consulta parametrizada"""
    try:
        with engine.connect() as conn:
            # Otra consulta parametrizada usando text()
            query = text("DELETE FROM estudiantes WHERE id = :id")
            conn.execute(query, {"id": estudiante_id})
            conn.commit()
        return RedirectResponse(url="/", status_code=303)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/estudiantes/{estudiante_id}")
async def obtener_estudiante(request: Request, estudiante_id: int):
    """Obtener detalles de un estudiante específico"""
    try:
        with engine.connect() as conn:
            query = text("SELECT * FROM estudiantes WHERE id = :id")
            result = conn.execute(query, {"id": estudiante_id})
            estudiante = result.fetchone()
            if estudiante is None:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        return templates.TemplateResponse(
            "estudiante.html",
            {"request": request, "estudiante": estudiante}
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/estudiantes/{estudiante_id}/editar")
async def formulario_editar_estudiante(request: Request, estudiante_id: int):
    """Mostrar formulario para editar un estudiante"""
    try:
        with engine.connect() as conn:
            query = text("SELECT * FROM estudiantes WHERE id = :id")
            result = conn.execute(query, {"id": estudiante_id})
            estudiante = result.fetchone()
            if estudiante is None:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        return templates.TemplateResponse(
            "editar_estudiante.html",
            {"request": request, "estudiante": estudiante}
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/estudiantes/{estudiante_id}/editar")
async def editar_estudiante(
    estudiante_id: int,
    nombre: str = Form(...),
    edad: int = Form(...),
    grado: str = Form(...)
):
    """Actualizar un estudiante existente usando una consulta parametrizada"""
    try:
        with engine.connect() as conn:
            # Consulta parametrizada para UPDATE
            query = text("""
                UPDATE estudiantes 
                SET nombre = :nombre, 
                    edad = :edad, 
                    grado = :grado 
                WHERE id = :id
            """)
            conn.execute(query, {
                "id": estudiante_id,
                "nombre": nombre,
                "edad": edad,
                "grado": grado
            })
            conn.commit()
        return RedirectResponse(url=f"/estudiantes/{estudiante_id}", status_code=303)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))