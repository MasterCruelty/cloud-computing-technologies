from flask import Flask
import os
from datetime import datetime

app = Flask(__name__)

SERVICE_NAME = os.getenv("SERVICE_NAME", "unknown-service")
INSTANCE_ID = os.getenv("INSTANCE_ID", "unknown-instance")

@app.route("/orders",methods=["GET"])
def orders():
    return f"""
    <html>
        <head>
            <title>{SERVICE_NAME}</title>
        </head>
        <body>
            <h1>{SERVICE_NAME}</h1>
            <p><strong>Instance ID:</strong> {INSTANCE_ID}</p>
            <p><strong>Timestamp:</strong> {datetime.now()}</p>
        </body>
    </html>
    """
   
@app.route("/health", methods=["GET"])
def health():
    return {"status": "UP", "service": SERVICE_NAME}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
