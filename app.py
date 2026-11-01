# """
# Main FastAPI Application Entrypoint.
# Initializes the application, loads ML artifacts on startup, registers API routes,
# configures CORS, and serves the static frontend.
# """
# from contextlib import asynccontextmanager
# from pathlib import Path
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse

# from api.config import settings, STATIC_DIR
# from api.service import service
# from api.routes import router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup: Load ML model, encoder, and feature columns into memory once
#     service.load_artifacts()
#     yield
#     # Shutdown logic if any needed


# app = FastAPI(
#     title=settings.app_name,
#     version=settings.app_version,
#     description=(
#         "Production-grade REST API and Web Interface for the Air Pollution PM2.5 Prediction System. "
#         "Powered by an Extreme Gradient Boosting (XGBoost) model trained on meteorological and air quality records."
#     ),
#     lifespan=lifespan,
#     docs_url="/docs",
#     redoc_url="/redoc",
#     openapi_url="/openapi.json"
# )

# # CORS configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include API routes directly at root level as required (/health, /predict, etc.)
# app.include_router(router)
# # Also include under /api prefix for standard REST convention
# app.include_router(router, prefix="/api")


# # Serve frontend static assets if static folder exists
# if STATIC_DIR.exists():
#     app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

#     @app.get("/", include_in_schema=False)
#     async def serve_index():
#         index_file = STATIC_DIR / "index.html"
#         if index_file.exists():
#             return FileResponse(str(index_file))
#         return {
#             "message": "Air Pollution Prediction API is running. Visit /docs for interactive documentation."
#         }


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app:app", host=settings.host, port=settings.port, reload=False)

"""
Main FastAPI Application Entrypoint.
Initializes the application, loads ML artifacts on startup, registers API routes,
configures CORS, and serves the static frontend.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from api.config import settings, STATIC_DIR
from api.service import service
from api.routes import router


# ============================================================
# Application Lifespan: Startup and Shutdown
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    print("\n============================================")
    print("       Starting AeroPredict API")
    print("============================================")

    # Load ML model, encoder, and feature columns
    service.load_artifacts()

    # Display application URLs
    print("\nAeroPredict API is ready!")
    print("--------------------------------------------")
    print(f"Web Interface : {settings.local_url}/")
    print(f"Swagger Docs  : {settings.docs_url}")
    print(f"Health Check  : {settings.health_url}")
    print("--------------------------------------------")
    print("Application startup completed successfully.")
    print("============================================\n")

    yield

    # Shutdown
    print("\nAeroPredict API is shutting down...")
    print("Application stopped.")


# ============================================================
# FastAPI Application Configuration
# ============================================================

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Production-grade REST API and Web Interface for the Air Pollution PM2.5 Prediction System. "
        "Powered by an Extreme Gradient Boosting (XGBoost) model trained on meteorological and air quality records."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# ============================================================
# CORS Configuration
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API Routes Registration
# ============================================================

# Include API routes directly at root level
app.include_router(router)

# Also include under /api prefix
app.include_router(router, prefix="/api")


# ============================================================
# Frontend Static Files
# ============================================================

if STATIC_DIR.exists():

    app.mount(
        "/static",
        StaticFiles(directory=str(STATIC_DIR)),
        name="static"
    )

    @app.get("/", include_in_schema=False)
    async def serve_index():

        index_file = STATIC_DIR / "index.html"

        if index_file.exists():
            return FileResponse(str(index_file))

        return {
            "message": (
                "Air Pollution Prediction API is running. "
                "Visit /docs for interactive documentation."
            )
        }


# ============================================================
# Run Application
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port,
        reload=False
    )
