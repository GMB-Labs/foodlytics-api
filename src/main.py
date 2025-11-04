from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text, inspect

from src.iam.infrastructure.external.auth0.auth0_machine_service import Auth0MachineService
from src.shared.infrastructure.persistence.sqlalchemy.engine import Base,engine

#importar los controllers papai (por bounded context)
from src.iam.interfaces.rest.hello_controller import HelloController
from src.iam.interfaces.rest.auth_controller import router as auth_router


app = FastAPI(
    title='Foodlytics API',
    version='1.0',
    description='API for Foodlytics application',
)

# Crea todas las tablas
Base.metadata.create_all(bind=engine)

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
hello_auth_service_impl = Auth0MachineService()
hello_controller = HelloController(auth_service=hello_auth_service_impl)

app.include_router(hello_controller.router,prefix=API_PREFIX)
app.include_router(auth_router, prefix=API_PREFIX)

#=========HEALTH & DB CHECK  ==========#
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-check")
def db_check():
    inspector = inspect(engine)
    print(inspector.get_table_names())
    with engine.connect() as conn:
        version = conn.execute(text("SELECT version();")).scalar()
        return {"database": "connected", "version": version,"tables": inspector.get_table_names()}


