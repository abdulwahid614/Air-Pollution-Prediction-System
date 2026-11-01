# """
# Configuration module for the Air Pollution Prediction API.
# Handles project paths, model file locations, and application settings.
# """
# import os
# from pathlib import Path
# from pydantic import BaseModel

# # Project Root is the parent directory of this 'api' package
# PROJECT_ROOT = Path(__file__).resolve().parent.parent

# # Model and preprocessor file paths
# MODEL_PATH = PROJECT_ROOT / "best_pm25_model.pkl"
# ENCODER_PATH = PROJECT_ROOT / "pm25_encoder.pkl"
# FEATURE_COLUMNS_PATH = PROJECT_ROOT / "pm25_feature_columns.pkl"
# DATASET_PATH = PROJECT_ROOT / "Beijing_PM25_Training_Ready_75896.csv"

# # Optional alternative models in project root
# XGBOOST_MODEL_PATH = PROJECT_ROOT / "xgboost_pm25_model.pkl"
# OPTIMIZED_XGBOOST_PATH = PROJECT_ROOT / "optimized_xgboost_pm25_model.pkl"
# RANDOM_FOREST_PATH = PROJECT_ROOT / "random_forest_pm25_model.pkl"

# # Static files directory
# STATIC_DIR = PROJECT_ROOT / "static"


# class Settings(BaseModel):
#     app_name: str = "AeroPredict - Air Pollution PM2.5 Prediction System"
#     app_version: str = "2.0.0"
#     target_name: str = "PM2.5 Concentration"
#     target_unit: str = "µg/m³"
#     host: str = os.getenv("HOST", "0.0.0.0")
#     port: int = int(os.getenv("PORT", "8000"))
#     debug: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")


# settings = Settings()

"""
Configuration module for the Air Pollution Prediction API.
Handles project paths, model file locations, and application settings.
"""

import os
from pathlib import Path
from pydantic import BaseModel

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Model and preprocessor file paths
MODEL_PATH = PROJECT_ROOT / "best_pm25_model.pkl"
ENCODER_PATH = PROJECT_ROOT / "pm25_encoder.pkl"
FEATURE_COLUMNS_PATH = PROJECT_ROOT / "pm25_feature_columns.pkl"
DATASET_PATH = PROJECT_ROOT / "Beijing_PM25_Training_Ready_75896.csv"

# Optional alternative models
XGBOOST_MODEL_PATH = PROJECT_ROOT / "xgboost_pm25_model.pkl"
OPTIMIZED_XGBOOST_PATH = PROJECT_ROOT / "optimized_xgboost_pm25_model.pkl"
RANDOM_FOREST_PATH = PROJECT_ROOT / "random_forest_pm25_model.pkl"

# Static files directory
STATIC_DIR = PROJECT_ROOT / "static"


class Settings(BaseModel):
    app_name: str = "AeroPredict - Air Pollution PM2.5 Prediction System"
    app_version: str = "2.0.0"
    target_name: str = "PM2.5 Concentration"
    target_unit: str = "µg/m³"

    # Docker / Uvicorn settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

    # Browser URLs
    local_url: str = "http://127.0.0.1:8000"
    docs_url: str = "http://127.0.0.1:8000/docs"
    health_url: str = "http://127.0.0.1:8000/health"

    debug: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")


settings = Settings()
