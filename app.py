from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection config
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "password")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route("/")
def home():
    return "Flask API is running."

@app.route("/users", methods=["GET"])
def get_users():
    print("GET /users called")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
                (data["name"], data["email"]))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id}), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET name=%s, email=%s WHERE id=%s",
                (data["name"], data["email"], user_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "User updated"})

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "User deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

