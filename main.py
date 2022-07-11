from flask import Flask, render_template
from flask_socketio import SocketIO, send
import json, time

app = Flask(__name__)
app.debug = True

socketio = SocketIO(app, cors_allowedorigins="*")

@socketio.on("message")
def handle_message(message):
    print("Received message : " + message)
    if message != "User connected !":
        send(message, broadcast=True)
    else:
        liste_data = json.load(open("messages.json", "r"))
        send(liste_data, broadcast=True, json=True)

@socketio.on("json")
def handle_message(data):
    date = time.asctime()
    data["time"] = date[4:16]
    print("Received json : ", data)
    liste_data = json.load(open("messages.json", "r"))
    liste_data.append(data)
    json_object = json.dumps(liste_data, indent = 4)
    open("messages.json", "w").write(json_object)
    send(liste_data, broadcast=True, json=True)

@app.route("/")
def index():
    return render_template("messagesScreen.html")


if __name__ == '__main__':
    socketio.run(app)