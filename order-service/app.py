from flask import Flask, request, render_template_string
import os
from datetime import datetime
import json

app = Flask(__name__)
data = "/data/orders.json"

SERVICE_NAME = os.getenv("SERVICE_NAME", "unknown-service")
INSTANCE_ID = os.getenv("INSTANCE_ID", "unknown-instance")

#caricamento file volume
def load_volume():
    if not os.path.exists(data):
        save_orders([])
        return []

    with open(data, "r") as f:
        data_json = json.load(f)
        
        if isinstance(data_json, dict) and "orders" in data_json:
            return data_json["orders"]
        elif isinstance(data_json, list):
            return data_json
        else:
            return []

#salvataggio dati nel file volume
def save_orders(orders):
    with open(data, "w") as f:
         json.dump({"orders": orders}, f, indent=4)


@app.route("/orders",methods=["GET","POST"])
def orders():

    orders = load_volume()

    if request.method == "POST":
        order = request.form.get("order")
        if order:
            orders.append(order)
            save_orders(orders)
            
    return render_template_string("""
        <html>
            <head>
                <title>{{ service_name }}</title>
            </head>
            <body>
                <h1>{{ service_name }}</h1>
                <p><strong>Instance ID:</strong> {{ instance_id }}</p>
                <p><strong>Timestamp:</strong> {{ timestamp }}</p>
        
                <form method="POST">
                    <input name="order" placeholder="New order">
                    <button type="submit">Add</button>
                </form>
                {% if orders %}
                   <ul>
                        {% for o in orders %}
                            <li>{{ o }}</li>
                        {% endfor %}
                   </ul>
                {% else %}
                    <p><em>No orders yet</em></p>
                {% endif %}            
            </body>
        </html>
    """, 
    orders=orders, 
    service_name=SERVICE_NAME, 
    instance_id=INSTANCE_ID, 
    timestamp=datetime.now())
   
@app.route("/health", methods=["GET"])
def health():
    return {"status": "UP", "service": SERVICE_NAME,"instance": INSTANCE_ID}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
