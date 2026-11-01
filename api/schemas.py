"""
Pydantic schemas for the Air Pollution Prediction API.
Validates input features and standardizes API responses.
"""
from enum import Enum
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field, model_validator


class StationName(str, Enum):
    """Supported monitoring stations in the Beijing combined dataset."""
    AOTIZHONGXIN = "Aotizhongxin"
    US_EMBASSY = "US_Embassy"


class PredictionRequest(BaseModel):
    """
    Input features for PM2.5 prediction matching the trained XGBoost model.
    Expected feature list:
    ['year', 'month', 'day', 'hour', 'DEWP', 'TEMP', 'PRES', 'station_Aotizhongxin', 'station_US_Embassy']
    """
    year: int = Field(
        ...,
        ge=2000,
        le=2100,
        description="Year of measurement (e.g. 2014)",
        examples=[2014]
    )
    month: int = Field(
        ...,
        ge=1,
        le=12,
        description="Month of measurement (1 to 12)",
        examples=[6]
    )
    day: int = Field(
        ...,
        ge=1,
        le=31,
        description="Day of the month (1 to 31)",
        examples=[15]
    )
    hour: int = Field(
        ...,
        ge=0,
        le=23,
        description="Hour of the day in 24-hour format (0 to 23)",
        examples=[12]
    )
    DEWP: float = Field(
        ...,
        ge=-60.0,
        le=50.0,
        description="Dew Point in degrees Celsius (°C)",
        examples=[10.0]
    )
    TEMP: float = Field(
        ...,
        ge=-50.0,
        le=60.0,
        description="Temperature in degrees Celsius (°C)",
        examples=[25.0]
    )
    PRES: float = Field(
        ...,
        ge=900.0,
        le=1100.0,
        description="Barometric Pressure in hectopascals (hPa)",
        examples=[1005.0]
    )
    station_Aotizhongxin: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Binary indicator for Aotizhongxin station (1.0 or 0.0)",
        examples=[0.0]
    )
    station_US_Embassy: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Binary indicator for US_Embassy station (1.0 or 0.0)",
        examples=[1.0]
    )
    station: Optional[str] = Field(
        default=None,
        description="Station name ('Aotizhongxin' or 'US_Embassy'). If provided, station columns are set automatically.",
        examples=["US_Embassy"]
    )

    @model_validator(mode="after")
    def resolve_station_features(self) -> "PredictionRequest":
        """
        Ensures station columns are properly set whether the user passes
        'station' by name or directly passes the one-hot columns.
        """
        # If station name was provided
        if self.station is not None:
            norm_name = str(self.station).strip().replace(" ", "_")
            if norm_name.lower() in ("aotizhongxin", "aoti"):
                self.station = StationName.AOTIZHONGXIN.value
                self.station_Aotizhongxin = 1.0
                self.station_US_Embassy = 0.0
            elif norm_name.lower() in ("us_embassy", "usembassy", "embassy", "us"):
                self.station = StationName.US_EMBASSY.value
                self.station_Aotizhongxin = 0.0
                self.station_US_Embassy = 1.0
            else:
                raise ValueError(
                    f"Unknown station '{self.station}'. Allowed values: {[s.value for s in StationName]}"
                )
        # If user directly specified one-hot columns without station name
        elif self.station_Aotizhongxin is not None or self.station_US_Embassy is not None:
            aoti = float(self.station_Aotizhongxin or 0.0)
            us = float(self.station_US_Embassy or 0.0)
            self.station_Aotizhongxin = aoti
            self.station_US_Embassy = us
            if aoti >= 0.5:
                self.station = StationName.AOTIZHONGXIN.value
            elif us >= 0.5:
                self.station = StationName.US_EMBASSY.value
            else:
                self.station = "Unknown"
        # If neither was specified, default to US_Embassy
        else:
            self.station = StationName.US_EMBASSY.value
            self.station_Aotizhongxin = 0.0
            self.station_US_Embassy = 1.0

        return self


class PredictionResponse(BaseModel):
    """
    Standard response payload for PM2.5 prediction.
    """
    status: str = Field(default="success", description="Prediction status")
    target_name: str = Field(default="PM2.5 Concentration", description="Target variable name")
    unit: str = Field(default="µg/m³", description="Measurement unit of the target")
    predicted_pm25: float = Field(..., description="Actual predicted PM2.5 concentration value")
    input_features: Dict[str, Any] = Field(..., description="Echoed input features used for inference")
    model_name: str = Field(default="XGBoost Regressor (best_pm25_model.pkl)", description="Model used for prediction")
    timestamp: str = Field(..., description="ISO 8601 timestamp of the prediction")
    execution_time_ms: float = Field(..., description="Model inference latency in milliseconds")


class HealthResponse(BaseModel):
    """
    System health and model readiness response.
    """
    status: str = Field(..., description="'healthy' if model is loaded and ready, otherwise 'degraded'")
    model_loaded: bool = Field(..., description="Whether best_pm25_model.pkl loaded successfully")
    encoder_loaded: bool = Field(..., description="Whether pm25_encoder.pkl loaded successfully")
    features_loaded: bool = Field(..., description="Whether pm25_feature_columns.pkl loaded successfully")
    service_ready: bool = Field(..., description="Whether the prediction service is ready")
    target_name: str = Field(..., description="Model target name")
    target_unit: str = Field(..., description="Model target unit")
    expected_features: List[str] = Field(..., description="Ordered feature column names")
    details: Optional[str] = None


class ModelEvaluationMetrics(BaseModel):
    """
    Evaluation metrics verified on the holdout test set (20% chronological split).
    """
    mae: float = Field(default=42.95, description="Mean Absolute Error in µg/m³")
    rmse: float = Field(default=61.62, description="Root Mean Squared Error in µg/m³")
    r2_score: float = Field(default=0.5348, description="R² Determination Coefficient")
    test_samples_count: int = Field(default=15180, description="Number of test records evaluated")
    train_split_ratio: float = Field(default=0.80, description="Chronological training split ratio")


class ModelInfoResponse(BaseModel):
    """
    Information about the trained machine learning pipeline.
    """
    model_type: str
    target_variable: str
    target_unit: str
    feature_columns: List[str]
    categorical_categories: Dict[str, List[str]]
    feature_importance: Dict[str, float]
    evaluation_metrics: ModelEvaluationMetrics


class SampleRecord(BaseModel):
    """
    A verified historical record for testing and demonstration.
    """
    name_en: str
    name_ar: str
    description_en: str
    description_ar: str
    features: Dict[str, Any]
    actual_pm25: Optional[float] = None
