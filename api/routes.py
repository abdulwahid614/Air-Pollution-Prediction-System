"""
API Route Handlers for Air Pollution Prediction.
Defines endpoints for health checking, prediction, model inspection, and historical stats.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from api.schemas import (
    PredictionRequest,
    PredictionResponse,
    HealthResponse,
    ModelInfoResponse,
    SampleRecord
)
from api.service import service

router = APIRouter(tags=["Air Pollution Prediction"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Service Health and Model Status",
    description="Returns API status, whether machine learning artifacts are loaded, and readiness to accept predictions."
)
async def health_check():
    is_ready = service.is_ready
    status_str = "healthy" if is_ready else "degraded"
    status_code = status.HTTP_200_OK if is_ready else status.HTTP_503_SERVICE_UNAVAILABLE

    response_data = HealthResponse(
        status=status_str,
        model_loaded=service.model_loaded,
        encoder_loaded=service.encoder_loaded,
        features_loaded=service.features_loaded,
        service_ready=is_ready,
        target_name="PM2.5 Concentration",
        target_unit="µg/m³",
        expected_features=service.feature_columns,
        details=service.load_error if not is_ready else "All ML artifacts loaded and active."
    )
    return JSONResponse(status_code=status_code, content=response_data.model_dump())


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict PM2.5 Air Pollution Concentration",
    description="Accepts meteorological and temporal inputs, applies exact training preprocessing, and returns the predicted PM2.5 level in µg/m³."
)
async def predict_pm25(request: PredictionRequest):
    if not service.is_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Prediction service is unavailable: {service.load_error or 'Model not loaded'}"
        )

    try:
        result = service.predict(request)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during prediction inference."
        )


@router.get(
    "/model-info",
    response_model=ModelInfoResponse,
    summary="Trained Model Architecture and Verified Metrics",
    description="Returns detailed information about the trained XGBoost model, feature importance, and test set evaluation metrics."
)
async def get_model_info():
    if not service.is_ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model metadata is unavailable because artifacts are not loaded."
        )
    return service.get_model_info()


@router.get(
    "/historical-stats",
    summary="Verified Historical Pollution Statistics",
    description="Returns verified monthly and hourly PM2.5 averages and station distribution stats derived from the Beijing combined dataset."
)
async def get_historical_stats() -> Dict[str, Any]:
    return {
        "status": "success",
        "dataset_name": "Beijing PM2.5 Combined Dataset (US Embassy & Aotizhongxin)",
        "records_count": 75896,
        "stats": service.historical_stats
    }


@router.get(
    "/sample-records",
    summary="Pre-configured Authentic Dataset Scenarios",
    description="Provides real, verified records from the dataset for quick testing and demonstration in the frontend."
)
async def get_sample_records() -> List[Dict[str, Any]]:
    return service.sample_records
