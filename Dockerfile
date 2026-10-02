ARG BASE_IMAGE=qa-base:v1
FROM ${BASE_IMAGE}

WORKDIR /app

COPY src/ src/
COPY resources/ resources/
COPY inputs/ inputs/
COPY Scripts/ Scripts/

EXPOSE 8006

CMD ["uvicorn", "src.api.web_app:app", "--host", "0.0.0.0", "--port", "8006"]
