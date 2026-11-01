# استخدام إصدار مستقر من Python
FROM python:3.12-slim

# إعداد بيئة Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تثبيت مكتبات النظام المطلوبة (OpenMP لـ XGBoost)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# تحديد مجلد التطبيق
WORKDIR /app

# نسخ وتثبيت المتطلبات
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --default-timeout=120 -r requirements.txt

# نسخ ملفات التطبيق
COPY . .

# منفذ FastAPI
EXPOSE 8000

# تشغيل التطبيق
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
