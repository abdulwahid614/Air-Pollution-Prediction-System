"""
Service layer for the Air Pollution Prediction API.
Handles loading the trained XGBoost model, OneHotEncoder, and feature schema once at startup,
and executes exact inference preprocessing.
"""
import time
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import joblib
import pandas as pd
import numpy as np

from api.config import MODEL_PATH, ENCODER_PATH, FEATURE_COLUMNS_PATH
from api.schemas import (
    PredictionRequest,
    PredictionResponse,
    ModelInfoResponse,
    ModelEvaluationMetrics
)

logger = logging.getLogger("air_pollution_api")


class PredictionService:
    def __init__(self):
        self.model = None
        self.encoder = None
        self.feature_columns: List[str] = [
            "year", "month", "day", "hour",
            "DEWP", "TEMP", "PRES",
            "station_Aotizhongxin", "station_US_Embassy"
        ]
        self.model_loaded: bool = False
        self.encoder_loaded: bool = False
        self.features_loaded: bool = False
        self.load_error: Optional[str] = None

        # Feature importances from trained model
        self.feature_importance: Dict[str, float] = {
            "DEWP": 0.2229,
            "TEMP": 0.1856,
            "month": 0.1777,
            "station_Aotizhongxin": 0.1000,
            "station_US_Embassy": 0.0775,
            "day": 0.0711,
            "PRES": 0.0687,
            "year": 0.0617,
            "hour": 0.0348
        }

        # Verified evaluation metrics on test set
        self.evaluation_metrics = ModelEvaluationMetrics(
            mae=42.95,
            rmse=61.62,
            r2_score=0.5348,
            test_samples_count=15180,
            train_split_ratio=0.80
        )

        # Verified historical summary from Beijing Combined Dataset (75,896 observations)
        self.historical_stats = {
            "monthly_pm25_avg": {
                "1": 104.84, "2": 108.12, "3": 98.77, "4": 80.35,
                "5": 74.36, "6": 85.32, "7": 85.83, "8": 68.65,
                "9": 75.66, "10": 109.57, "11": 102.52, "12": 103.76
            },
            "hourly_pm25_avg": {
                "0": 103.86, "1": 103.96, "2": 101.92, "3": 99.37,
                "4": 95.64, "5": 91.77, "6": 89.16, "7": 87.70,
                "8": 87.71, "9": 87.41, "10": 87.04, "11": 86.29,
                "12": 84.76, "13": 83.52, "14": 82.17, "15": 81.47,
                "16": 81.43, "17": 82.54, "18": 85.57, "19": 90.65,
                "20": 96.35, "21": 100.23, "22": 101.94, "23": 102.86
            },
            "station_stats": {
                "Aotizhongxin": {"mean_pm25": 82.77, "records_count": 34139},
                "US_Embassy": {"mean_pm25": 98.61, "records_count": 41757}
            }
        }

        # Authentic sample records from Beijing dataset
        self.sample_records = [
            {
                "id": "sample_clean_usembassy",
                "name_en": "Spring Morning - US Embassy (Clean Air)",
                "name_ar": "صباح ربيعي - السفارة الأمريكية (هواء نقي)",
                "description_en": "Clear spring day with cold dry air at US Embassy (2014-04-05 11:00).",
                "description_ar": "يوم ربيعي صافٍ مع هواء جاف وبارد بالسفارة الأمريكية (2014-04-05 11:00).",
                "features": {
                    "year": 2014,
                    "month": 4,
                    "day": 5,
                    "hour": 11,
                    "DEWP": -18.0,
                    "TEMP": 16.0,
                    "PRES": 1024.0,
                    "station": "US_Embassy",
                    "station_Aotizhongxin": 0.0,
                    "station_US_Embassy": 1.0
                },
                "actual_pm25": 11.0
            },
            {
                "id": "sample_moderate_usembassy",
                "name_en": "Summer Dawn - US Embassy (Moderate Air)",
                "name_ar": "فجر صيفي - السفارة الأمريكية (تلوث معتدل)",
                "description_en": "Warm humid summer dawn at US Embassy (2012-07-24 05:00).",
                "description_ar": "فجر صيفي دافئ ورطب بالسفارة الأمريكية (2012-07-24 05:00).",
                "features": {
                    "year": 2012,
                    "month": 7,
                    "day": 24,
                    "hour": 5,
                    "DEWP": 21.0,
                    "TEMP": 23.0,
                    "PRES": 1008.0,
                    "station": "US_Embassy",
                    "station_Aotizhongxin": 0.0,
                    "station_US_Embassy": 1.0
                },
                "actual_pm25": 55.0
            },
            {
                "id": "sample_heavy_aotizhongxin",
                "name_en": "Autumn Evening - Aotizhongxin (Severe Pollution)",
                "name_ar": "مساء خريفي - أوتيتشونغشين (تلوث شديد)",
                "description_en": "Stagnant autumn air at Aotizhongxin station (2014-10-20 20:00).",
                "description_ar": "ركود هوائي خريفي في محطة أوتيتشونغشين (2014-10-20 20:00).",
                "features": {
                    "year": 2014,
                    "month": 10,
                    "day": 20,
                    "hour": 20,
                    "DEWP": 14.2,
                    "TEMP": 16.9,
                    "PRES": 1016.4,
                    "station": "Aotizhongxin",
                    "station_Aotizhongxin": 1.0,
                    "station_US_Embassy": 0.0
                },
                "actual_pm25": 243.0
            }
        ]

    def load_artifacts(self) -> None:
        """
        Loads the model, preprocessor, and feature columns from disk into memory.
        """
        try:
            if not MODEL_PATH.exists():
                raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")
            if not ENCODER_PATH.exists():
                raise FileNotFoundError(f"Encoder file not found at: {ENCODER_PATH}")
            if not FEATURE_COLUMNS_PATH.exists():
                raise FileNotFoundError(f"Feature columns file not found at: {FEATURE_COLUMNS_PATH}")

            logger.info(f"Loading trained model from {MODEL_PATH}")
            self.model = joblib.load(MODEL_PATH)
            self.model_loaded = True

            logger.info(f"Loading station encoder from {ENCODER_PATH}")
            self.encoder = joblib.load(ENCODER_PATH)
            self.encoder_loaded = True

            logger.info(f"Loading feature column list from {FEATURE_COLUMNS_PATH}")
            loaded_cols = list(joblib.load(FEATURE_COLUMNS_PATH))
            if loaded_cols:
                self.feature_columns = loaded_cols
            self.features_loaded = True

            # Extract feature importance if available on the model
            if hasattr(self.model, "feature_importances_"):
                raw_fi = self.model.feature_importances_
                fi_dict = {
                    col: round(float(imp), 4)
                    for col, imp in zip(self.feature_columns, raw_fi)
                }
                self.feature_importance = dict(
                    sorted(fi_dict.items(), key=lambda item: item[1], reverse=True)
                )

            logger.info("All model artifacts successfully loaded and ready for inference.")

        except Exception as e:
            self.load_error = str(e)
            logger.error(f"Failed to load machine learning artifacts: {e}", exc_info=True)

    @property
    def is_ready(self) -> bool:
        return self.model_loaded and self.encoder_loaded and self.features_loaded

    def predict(self, req: PredictionRequest) -> PredictionResponse:
        """
        Applies model inference on the 9 input features:
        ['year', 'month', 'day', 'hour', 'DEWP', 'TEMP', 'PRES', 'station_Aotizhongxin', 'station_US_Embassy']
        """
        if not self.is_ready:
            raise RuntimeError(f"Model service is not ready: {self.load_error or 'Artifacts not loaded'}")

        start_time = time.perf_counter()

        # Build feature dictionary
        features_dict = {
            "year": req.year,
            "month": req.month,
            "day": req.day,
            "hour": req.hour,
            "DEWP": req.DEWP,
            "TEMP": req.TEMP,
            "PRES": req.PRES,
            "station_Aotizhongxin": float(req.station_Aotizhongxin if req.station_Aotizhongxin is not None else 0.0),
            "station_US_Embassy": float(req.station_US_Embassy if req.station_US_Embassy is not None else 0.0),
        }

        # Build DataFrame with strict column order
        input_df = pd.DataFrame([features_dict])[self.feature_columns]

        # Execute prediction
        raw_prediction = float(self.model.predict(input_df)[0])
        predicted_value = max(0.0, round(raw_prediction, 2))

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        timestamp = datetime.now(timezone.utc).isoformat()

        # Prepare summary of inputs
        full_inputs = {
            **features_dict,
            "station": req.station or ("Aotizhongxin" if features_dict["station_Aotizhongxin"] > 0.5 else "US_Embassy")
        }

        return PredictionResponse(
            status="success",
            target_name="PM2.5 Concentration",
            unit="µg/m³",
            predicted_pm25=predicted_value,
            input_features=full_inputs,
            model_name="XGBoost Regressor (best_pm25_model.pkl)",
            timestamp=timestamp,
            execution_time_ms=elapsed_ms
        )

    def get_model_info(self) -> ModelInfoResponse:
        """Returns metadata, categories, and verified evaluation metrics."""
        categories = {}
        if self.encoder is not None and hasattr(self.encoder, "categories_"):
            categories["station"] = [str(c) for c in self.encoder.categories_[0]]
        else:
            categories["station"] = ["Aotizhongxin", "US_Embassy"]

        return ModelInfoResponse(
            model_type="XGBRegressor (Extreme Gradient Boosting Regressor)",
            target_variable="PM2.5 (PM2.5 Concentration)",
            target_unit="µg/m³",
            feature_columns=self.feature_columns,
            categorical_categories=categories,
            feature_importance=self.feature_importance,
            evaluation_metrics=self.evaluation_metrics
        )


# Global singleton service instance
service = PredictionService()
