"""
Automated Unit and Integration Tests for Air Pollution Prediction API.
Verifies health endpoint, prediction logic with the 9 features, validation errors, and model consistency.
"""
import pytest
from fastapi.testclient import TestClient
from app import app
from api.service import service

client = TestClient(app)


def setup_module(module):
    """Ensure artifacts are loaded before running tests."""
    service.load_artifacts()


def test_health_endpoint():
    """Verify /health returns 200 and reports model ready with 9 features."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert data["encoder_loaded"] is True
    assert data["features_loaded"] is True
    assert data["service_ready"] is True
    assert data["target_name"] == "PM2.5 Concentration"
    assert data["target_unit"] == "µg/m³"
    assert len(data["expected_features"]) == 9
    assert data["expected_features"] == [
        "year", "month", "day", "hour",
        "DEWP", "TEMP", "PRES",
        "station_Aotizhongxin", "station_US_Embassy"
    ]


def test_predict_endpoint_valid_sample_with_station_name():
    """
    Verify valid prediction request using station name.
    """
    payload = {
        "year": 2014,
        "month": 6,
        "day": 15,
        "hour": 12,
        "DEWP": 10.0,
        "TEMP": 25.0,
        "PRES": 1005.0,
        "station": "US_Embassy"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["target_name"] == "PM2.5 Concentration"
    assert data["unit"] == "µg/m³"
    assert isinstance(data["predicted_pm25"], float)
    assert data["predicted_pm25"] > 0
    assert data["execution_time_ms"] > 0
    assert data["input_features"]["station_US_Embassy"] == 1.0
    assert data["input_features"]["station_Aotizhongxin"] == 0.0


def test_predict_endpoint_direct_onehot_station():
    """
    Verify prediction works when user sends direct one-hot features:
    ['year', 'month', 'day', 'hour', 'DEWP', 'TEMP', 'PRES', 'station_Aotizhongxin', 'station_US_Embassy']
    """
    payload = {
        "year": 2014,
        "month": 10,
        "day": 20,
        "hour": 20,
        "DEWP": 14.2,
        "TEMP": 16.9,
        "PRES": 1016.4,
        "station_Aotizhongxin": 1.0,
        "station_US_Embassy": 0.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["predicted_pm25"] > 0
    assert data["input_features"]["station_Aotizhongxin"] == 1.0
    assert data["input_features"]["station_US_Embassy"] == 0.0


def test_predict_endpoint_aotizhongxin_name():
    """Verify prediction works with Aotizhongxin station name."""
    payload = {
        "year": 2015,
        "month": 9,
        "day": 13,
        "hour": 7,
        "DEWP": 12.3,
        "TEMP": 15.5,
        "PRES": 1013.1,
        "station": "Aotizhongxin"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["predicted_pm25"] > 0
    assert data["input_features"]["station_Aotizhongxin"] == 1.0


def test_predict_validation_invalid_month():
    """Verify 422 Unprocessable Entity when month is out of range."""
    payload = {
        "year": 2014,
        "month": 13,  # Invalid month
        "day": 15,
        "hour": 12,
        "DEWP": 10.0,
        "TEMP": 25.0,
        "PRES": 1005.0,
        "station": "US_Embassy"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_validation_invalid_station():
    """Verify 422 Unprocessable Entity when station is unknown."""
    payload = {
        "year": 2014,
        "month": 6,
        "day": 15,
        "hour": 12,
        "DEWP": 10.0,
        "TEMP": 25.0,
        "PRES": 1005.0,
        "station": "NonExistentStation"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_validation_missing_field():
    """Verify 422 Unprocessable Entity when required field is missing."""
    payload = {
        "year": 2014,
        "month": 6,
        # 'day' is missing
        "hour": 12,
        "DEWP": 10.0,
        "TEMP": 25.0,
        "PRES": 1005.0,
        "station": "US_Embassy"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_model_info_endpoint():
    """Verify /model-info returns architecture details and verified metrics."""
    response = client.get("/model-info")
    assert response.status_code == 200
    data = response.json()
    assert "XGBRegressor" in data["model_type"]
    assert data["evaluation_metrics"]["mae"] == 42.95
    assert data["evaluation_metrics"]["rmse"] == 61.62
    assert data["evaluation_metrics"]["r2_score"] == 0.5348
    assert len(data["feature_columns"]) == 9


def test_historical_stats_endpoint():
    """Verify /historical-stats returns the combined dataset record count."""
    response = client.get("/historical-stats")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["records_count"] == 75896
    assert "Aotizhongxin" in data["stats"]["station_stats"]
    assert "US_Embassy" in data["stats"]["station_stats"]
