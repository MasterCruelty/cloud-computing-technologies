FROM python:3.11-slim

# Imposta la directory di lavoro
WORKDIR /users

# Copia le dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'applicazione
COPY app.py .

# Espone la porta usata da Flask
EXPOSE 5000

# Avvia il servizio
CMD ["python", "app.py"]
