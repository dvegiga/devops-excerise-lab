from flask import Flask, jsonify
import socket, os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Hello from the DevOps lab",
        "hostname": socket.gethostname(),
        "version": os.getenv("APP_VERSION", "v1")
    })

@app.route("/healthz")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
