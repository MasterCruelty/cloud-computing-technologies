import requests
import time
import json
from datetime import datetime

# rotte interne microservizi su /health
services = {
    "user-service": [
        "http://user-service-1:5000/health",
        "http://user-service-2:5000/health"
    ],
    "orders-service": [
        "http://orders-service-1:5000/health",
        "http://orders-service-2:5000/health"
    ]
}

#ciclo infinito che ogni 10 secondi effettua richieste verso endpoint interno /health su tutte le istanze.
while True:
    status = {}

    for service, urls in services.items():
        status[service] = {}
        for url in urls:
            instance = url.split("//")[1]
            try:
                r = requests.get(url, timeout=2)
                status[service][instance] = "UP"
            except:
                status[service][instance] = "DOWN"

    print(json.dumps(status, indent=4), flush=True)
    print(datetime.now())
    time.sleep(20)  # ogni 10 secondi ripete il check
