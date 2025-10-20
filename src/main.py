from fastapi import FastAPI
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware

# importar los controllers papai (por bounded context)
from src.shared.infrastructure.db.engine import engine
# algo asi typeshii from src.controllers.user_controller import router as user_router


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

# registro de las rutas de los endpoints




#=========HEALTH & DB CHECK  ==========#
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-check")
def db_check():
    with engine.connect() as conn:
        version = conn.execute(text("SELECT version();")).scalar()
        return {"database": "connected", "version": version}
