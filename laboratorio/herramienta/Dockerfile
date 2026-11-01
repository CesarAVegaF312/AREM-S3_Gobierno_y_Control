# Python para la herramienta y el binario de Conftest copiado de su imagen oficial.
FROM openpolicyagent/conftest:v0.71.1 AS conftest

FROM python:3.12-slim
COPY --from=conftest /conftest /usr/local/bin/conftest
WORKDIR /app
COPY gobierno.py .
ENTRYPOINT ["python", "/app/gobierno.py"]
