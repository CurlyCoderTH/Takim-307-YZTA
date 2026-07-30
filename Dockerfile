# CogniTrace — konteyner imajı (backlog: 'Containerize Streamlit application')
# Playwright'ın resmî Python imajı: Chromium ve tüm sistem bağımlılıkları hazır
# gelir; 'playwright install' derdi olmadan URL yakalama konteynerde de çalışır.
FROM mcr.microsoft.com/playwright/python:v1.49.0-noble

WORKDIR /cognitrace

# Önce bağımlılıklar (katman önbelleği: kod değişince pip tekrar koşmaz)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && playwright install chromium

# Uygulama kodu
COPY app/ .

EXPOSE 8501

# GEMINI_API_KEY çalıştırma anında verilir (imaja gömülmez!):
#   docker build -t cognitrace .
#   docker run -p 8501:8501 -e GEMINI_API_KEY=anahtar cognitrace
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
