from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import sqlite3, os, datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# DB
conn = sqlite3.connect("chat.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS messages (user TEXT, device TEXT, msg TEXT, time TEXT)")
conn.commit()

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message")
def handle_message(data):
    user = data["user"]
    device = data["device"]
    msg = data["msg"]
    time = datetime.datetime.now().strftime("%H:%M")

    c.execute("INSERT INTO messages VALUES (?,?,?,?)", (user, device, msg, time))
    conn.commit()

    send({"user":user,"device":device,"msg":msg,"time":time}, broadcast=True)

@socketio.on("typing")
def typing(data):
    emit("typing", data, broadcast=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    socketio.run(app, host="0.0.0.0", port=port)