from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text, inspect
import logging
from src.iam.infrastructure.external.auth0.auth0_machine_service import Auth0MachineService
from src.meal_recognition.interfaces.rest.food_recognition_controller import MealRecognitionController
from src.shared.infrastructure.persistence.sqlalchemy.engine import Base,engine
from src.shared.infrastructure.dependencies import get_event_bus
from src.profile.application.internal.eventhandlers import register_profile_event_handlers

#importar los controllers papai (por bounded context)
from src.iam.interfaces.rest.hello_controller import HelloController
from src.iam.interfaces.rest.auth_controller import router as auth_router
from src.profile.interfaces.rest.profile_controller import ProfileController


app = FastAPI(
    title='Foodlytics API',
    version='1.0',
    description='API for Foodlytics application',
)
logging.getLogger("src.shared.infrastructure.events.in_memory_event_bus").setLevel(logging.DEBUG)

logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
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
profile_controller = ProfileController()

# register cross-context event handlers
register_profile_event_handlers(get_event_bus())

app.include_router(hello_controller.router,prefix=API_PREFIX)
app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(profile_controller.router, prefix=API_PREFIX)


meal_controller = MealRecognitionController()
app.include_router(meal_controller.router)

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


