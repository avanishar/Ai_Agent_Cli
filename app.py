import os
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, Response, send_from_directory
from dotenv import load_dotenv

load_dotenv()

import agent
import history as hist

app = Flask(__name__)
hist.init_db()

OUTPUTS_DIR = Path("outputs")

# ─── Web UI Routes ────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/outputs/<filename>")
def download_file(filename):
    return send_from_directory(OUTPUTS_DIR.absolute(), filename, as_attachment=True)

# ─── File Generation ──────────────────────────────────────

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    file_type = data.get("type", "article")
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    try:
        filepath, filename = agent.generate_file(file_type, topic)
        hist.log_generation(file_type, topic, filename)
        return jsonify({"filename": filename, "download_url": f"/outputs/{filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─── File Editing ─────────────────────────────────────────

@app.route("/api/edit", methods=["POST"])
def edit():
    data = request.json
    filename = data.get("filename", "").strip()
    instruction = data.get("instruction", "").strip()

    if not filename or not instruction:
        return jsonify({"error": "Filename and instruction are required"}), 400

    try:
        result = agent.edit_file(filename, instruction)
        return jsonify({"message": result})
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─── Chat with Streaming ──────────────────────────────────

@app.route("/api/chat/stream")
def chat_stream():
    message = request.args.get("message", "").strip()
    if not message:
        return Response("data: [DONE]\n\n", mimetype="text/event-stream")

    hist.log_chat("user", message)

    def generate_stream():
        full_reply = ""
        try:
            for chunk in agent.chat_stream(message):
                full_reply += chunk
                yield f"data: {json.dumps({'text': chunk})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        finally:
            hist.log_chat("assistant", full_reply)
            yield "data: [DONE]\n\n"

    return Response(
        generate_stream(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )

@app.route("/api/chat/clear", methods=["POST"])
def clear_chat():
    agent.clear_chat()
    return jsonify({"message": "Chat cleared"})

# ─── History ──────────────────────────────────────────────

@app.route("/api/history")
def get_history():
    return jsonify(hist.get_history())

@app.route("/api/history/clear", methods=["POST"])
def clear_history():
    hist.clear_history()
    return jsonify({"message": "History cleared"})

# ─── List output files ────────────────────────────────────

@app.route("/api/files")
def list_files():
    files = sorted(OUTPUTS_DIR.iterdir(), key=lambda f: f.stat().st_mtime, reverse=True)
    return jsonify([f.name for f in files if f.is_file()])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
