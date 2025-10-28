from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text

from src.iam.infrastructure.external.auth0.auth0_machine_service import Auth0MachineService
from src.shared.infrastructure.persistence.sqlalchemy.engine import engine

#importar los controllers papai (por bounded context)
from src.iam.interfaces.rest.auth_controller import AuthController



app = FastAPI(
    title='Foodlytics API',
    version='1.0',
    description='API for Foodlytics application',
)

# Configurar CORS ======DEVELLOPMENT ONLY=======
# TODO: configurar adecuadamente cuando se tenga un despliegue con dominio especifico
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = '/api/v1'

# registro de las rutas de los endpoints typeshii
    #===EJEMPLO===
    #app.include_router(iam_controller, prefix="/auth", tags=["IAM"])
auth_service_impl = Auth0MachineService()
auth_controller = AuthController(auth_service=auth_service_impl) # <--- La inyección ocurre aquí
app.include_router(auth_controller.router,prefix=API_PREFIX)

#=========HEALTH & DB CHECK  ==========#
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-check")
def db_check():
    with engine.connect() as conn:
        version = conn.execute(text("SELECT version();")).scalar()
        return {"database": "connected", "version": version}
