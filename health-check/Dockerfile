FROM python:3.11-slim

WORKDIR /health-check

COPY healthcheck.py .

RUN pip install requests

CMD ["python", "-u", "healthcheck.py"]

