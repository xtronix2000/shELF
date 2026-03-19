import uuid
import threading
import json
import docker
from pathlib import Path
from flask import Flask, request, redirect, jsonify, render_template

from main import run_analysis
from sandbox.runner import build_image, run_build

app = Flask(__name__, template_folder="templates")


SOURCES_DIR = Path(__file__).parent.parent / "sources"
SOURCES_DIR.mkdir(exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_route():
    if "archive" not in request.files:
        return jsonify({"error": "Файл не загружен"}), 400

    file = request.files["archive"]

    if not file.filename:
        return jsonify({"error": "Пустое имя файла"}), 400

    # создаём директорию для этой задачи
    task_id = str(uuid.uuid4())[:8]
    project_path = SOURCES_DIR / task_id
    project_path.mkdir()

    # сохраняем архив
    archive_path = project_path / file.filename
    file.save(archive_path)

    # запускаем в фоне
    def job():
        client = docker.from_env()
        build_image(client)
        success = run_build(client, project_path)
        if success:
            run_analysis(project_path)

    thread = threading.Thread(target=job)
    thread.daemon = True
    thread.start()

    return redirect(f"/task/{task_id}")

@app.route("/task/<task_id>")
def task_page(task_id):
    project_path = SOURCES_DIR / task_id
    result_file = project_path / "interpreters.json"

    if not project_path.exists():
        status = "not_found"
        result = None
    elif not (project_path / "result").exists():
        status = "building"
        result = None
    elif not result_file.exists():
        status = "analyzing"
        result = None
    else:
        status = "done"
        result = json.loads(result_file.read_text())

    return render_template("result.html", task_id=task_id, status=status, result=result)


@app.route("/api/status/<task_id>")
def api_status(task_id):
    project_path = SOURCES_DIR / task_id
    result_file = project_path / "interpreters.json"

    if not project_path.exists():
        status = "not_found"
    elif not (project_path / "result").exists():
        status = "building"
    elif not result_file.exists():
        status = "analyzing"
    else:
        status = "done"

    return jsonify({"task_id": task_id, "status": status})