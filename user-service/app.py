from flask import Flask, request, render_template_string
import os
from datetime import datetime
import json

app = Flask(__name__)
data = "/data/users.json"

SERVICE_NAME = os.getenv("SERVICE_NAME", "unknown-service")
INSTANCE_ID = os.getenv("INSTANCE_ID", "unknown-instance")

#caricamento file volume
def load_volume():
    if not os.path.exists(data):
        save_users([])
        return []

    with open(data, "r") as f:
        data_json = json.load(f)
        
        if isinstance(data_json, dict) and "users" in data_json:
            return data_json["users"]
        elif isinstance(data_json, list):
            return data_json
        else:
            return []

#salvataggio dati nel file volume
def save_users(users):
    with open(data, "w") as f:
         json.dump({"users": users}, f, indent=4)





@app.route("/users",methods=["GET","POST"])
def users():
    
    users = load_volume()

    if request.method == "POST":
        user = request.form.get("user")
        if user:
            users.append(user)
            save_users(users)
            
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
                    <input name="user" placeholder="New user">
                    <button type="submit">Add</button>
                </form>
                {% if users %}
                   <ul>
                        {% for o in users %}
                            <li>{{ o }}</li>
                        {% endfor %}
                   </ul>
                {% else %}
                    <p><em>No users yet</em></p>
                {% endif %}            
            </body>
        </html>
    """, 
    users=users, 
    service_name=SERVICE_NAME, 
    instance_id=INSTANCE_ID, 
    timestamp=datetime.now())

@app.route("/health", methods=["GET"])
def health():
    return {"status": "UP", "service": SERVICE_NAME,"instance": INSTANCE_ID}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
