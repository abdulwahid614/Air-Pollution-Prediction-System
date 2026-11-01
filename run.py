# """
# Convenient one-command launcher for the Air Pollution Prediction System.
# Runs the FastAPI application and serves both the API and interactive Web UI.
# """
# import sys
# import uvicorn
# from api.config import settings

# if __name__ == "__main__":
#     print("=" * 60)
#     print("  Starting Air Pollution Prediction System (AeroPredict)")
#     print(f"  Target: {settings.target_name} ({settings.target_unit})")
#     print(f"  Web Interface : http://{settings.host}:{settings.port}/")
#     print(f"  API Swagger UI: http://{settings.host}:{settings.port}/docs")
#     print(f"  Health Check  : http://{settings.host}:{settings.port}/health")
#     print("=" * 60)
#     uvicorn.run("app:app", host=settings.host, port=settings.port, reload=False)

"""
Convenient one-command launcher for the Air Pollution Prediction System.
Runs the FastAPI application and serves both the API and interactive Web UI.
"""

import sys
import uvicorn
from api.config import settings

if __name__ == "__main__":
    host = "127.0.0.1"

    print("=" * 60)
    print("  Starting Air Pollution Prediction System (AeroPredict)")
    print(f"  Target: {settings.target_name} ({settings.target_unit})")
    print(f"  Web Interface : http://{host}:{settings.port}/")
    print(f"  API Swagger UI: http://{host}:{settings.port}/docs")
    print(f"  Health Check  : http://{host}:{settings.port}/health")
    print("=" * 60)

    uvicorn.run(
        "app:app",
        host=host,
        port=settings.port,
        reload=False
    )
