# Tutorial SQL Educativo con FastAPI

Esta es una aplicación web simple diseñada para enseñar conceptos básicos de SQL a estudiantes de de grado 11.

## Características Principales

- CRUD básico de estudiantes (Create, Read, Update, Delete)
- Interfaz web intuitiva y educativa
- Visualización de consultas SQL en la interfaz
- Manejo de errores básico
- Consultas parametrizadas seguras

## Conceptos SQL Demostrados

1. **CREATE TABLE**
   - Creación de tabla con restricciones
   - Tipos de datos básicos (INTEGER, TEXT)
   - Claves primarias y AUTO_INCREMENT

2. **INSERT**
   - Inserción de datos con valores parametrizados
   - Validación de datos

3. **SELECT**
   - Consultas básicas
   - Filtrado con WHERE
   - Ordenamiento con ORDER BY

4. **DELETE**
   - Eliminación de registros
   - Uso de condiciones WHERE

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **SQLite**: Base de datos simple y portátil
- **SQLAlchemy**: ORM con soporte para consultas SQL puras
- **Jinja2**: Motor de plantillas para HTML
- **Bootstrap**: Framework CSS para el diseño

## Instalación

1. Asegúrate de tener Python 3.8+ instalado

2. Instala las dependencias:
   ```bash
   uv add "fastapi[standard]" sqlalchemy
   ```

3. Ejecuta la aplicación:
   ```bash
   fastapi dev main.py
   ```

4. Abre http://localhost:8000 en tu navegador

## Estructura del Proyecto

```
.
├── main.py           # Lógica principal y rutas
├── templates/        # Plantillas HTML
│   ├── index.html    # Página principal
│   └── estudiante.html # Detalles de estudiante
├── static/          # Archivos estáticos (si se necesitan)
└── sql_app.db       # Base de datos SQLite
```

## Características de Seguridad

1. **Consultas Parametrizadas**
   - Prevención de inyección SQL
   - Uso de SQLAlchemy text() para consultas seguras

2. **Validación de Datos**
   - Restricciones en la base de datos
   - Validación de formularios

## Notas Educativas

- Las consultas SQL se muestran en la interfaz para propósitos educativos
- Se utilizan consultas SQL puras (en lugar de ORM) para mejor comprensión
- Los comentarios en el código explican conceptos importantes
- La interfaz es simple pero moderna para mantener el foco en el aprendizaje

## Próximos Pasos Sugeridos

1. Agregar más tipos de consultas SELECT (GROUP BY, JOIN)
2. Implementar actualización de registros (UPDATE)
3. Añadir más tablas para relaciones
4. Incluir ejemplos de índices y optimización

## Contribución

Si encuentras errores o tienes sugerencias, no dudes en abrir un issue o enviar un pull request.