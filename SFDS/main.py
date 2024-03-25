import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from apps.config import settings
from fastapi.middleware.cors import CORSMiddleware





def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        description=settings.PROJECT_DESCRIPTION,
    )

    if not os.path.exists(settings.MEDIA_PATH):
        os.makedirs(settings.MEDIA_PATH)

    media_directory = Path(settings.MEDIA_PATH)
    app.mount("/media", StaticFiles(directory=media_directory), name="media")



    origins = [
        "http://localhost:3000",
        "https://localhost:3000",
        "http://127.0.0.1:3000"
    ]


    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    return app

def initialize_routers(app: FastAPI) -> FastAPI:
    from apps.apis.v1.auth.routes import router as auth_router
    from apps.apis.v1.users.profile_routes import router as profile_router

    app.include_router(auth_router, prefix="/api", tags=['auth'])
    app.include_router(profile_router, prefix="/api", tags=['profile'])

    return app

app = get_application()
app = initialize_routers(app=app)


@app.get("/")
async def home():
    return {"status": f"{settings.APP_ENV} is running" }
