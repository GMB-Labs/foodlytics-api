from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text, inspect

# Importaciones internas
from src.shared.infrastructure.persistence.sqlalchemy.engine import Base, engine
from src.iam.infrastructure.external.auth0.auth0_machine_service import Auth0MachineService

# Importar los controladores (bounded contexts)
from src.iam.interfaces.rest.hello_controller import HelloController
from src.iam.interfaces.rest.auth_controller import router as auth_router
from src.iam.interfaces.rest.auth_controller import AuthController
from src.payments.interfaces.rest.payment_controller import router as payments_router


# ==============================================
#  Configuración principal de la aplicación
# ==============================================
app = FastAPI(
    title='Foodlytics API',
    version='1.0',
    description='API for Foodlytics application',
)
logging.getLogger("src.shared.infrastructure.events.in_memory_event_bus").setLevel(logging.DEBUG)

# Crear todas las tablas definidas en los modelos Base
Base.metadata.create_all(bind=engine)

# ==============================================
#  Configuración de CORS (solo desarrollo)
# ==============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: limitar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prefijo global de versión
API_PREFIX = "/api/v1"

# ==============================================
#  Registro de controladores (rutas)
# ==============================================
hello_auth_service_impl = Auth0MachineService()
hello_controller = HelloController(auth_service=hello_auth_service_impl)
profile_controller = ProfileController()

# register cross-context event handlers
register_profile_event_handlers(get_event_bus())

app.include_router(hello_controller.router,prefix=API_PREFIX)
app.include_router(auth_router, prefix=API_PREFIX)
# Rutas de IAM
app.include_router(hello_controller.router, prefix=API_PREFIX)
# Si tienes AuthController también puedes registrar:
# app.include_router(AuthController().router, prefix=API_PREFIX)

# Rutas de Pagos (Culqi)
app.include_router(payments_router, prefix=API_PREFIX)

# ==============================================
#  Endpoints de diagnóstico
# ==============================================
@app.get("/health")
def health():
    """Verifica que el servicio esté corriendo."""
    return {"status": "ok"}

@app.get("/db-check")
def db_check():
    """Verifica conexión a la base de datos."""
    inspector = inspect(engine)
    with engine.connect() as conn:
        version = conn.execute(text("SELECT version();")).scalar()
        return {
            "database": "connected",
            "version": version,
            "tables": inspector.get_table_names()
        }

# ==============================================
#  Punto de entrada (solo si se ejecuta directamente)
# ==============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
