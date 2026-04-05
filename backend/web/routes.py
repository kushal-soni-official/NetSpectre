from flask import Blueprint, render_template, request, jsonify, send_from_directory
from backend.tasks.scan_tasks import run_network_scan
from backend.config import Config
import os

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    return render_template('index.html')

@web_bp.route('/api/scan/start', methods=['POST'])
def start_scan():
    data = request.json
    target = data.get('target')
    mode = data.get('mode', 'light')  # 'light' or 'deep'
    
    if not target:
        return jsonify({"error": "Target subnet is required"}), 400
        
    task = run_network_scan.delay(target, mode)
    return jsonify({"task_id": task.id}), 202

@web_bp.route('/api/scan/<task_id>/status', methods=['GET'])
def get_status(task_id):
    task = run_network_scan.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {"state": task.state, "status": "Pending..."}
    elif task.state != 'FAILURE':
        response = {
            "state": task.state,
            "status": task.info.get('status', '') if task.info else '',
        }
        if task.state == 'SUCCESS':
            response['result'] = task.result
    else:
        response = {"state": task.state, "status": str(task.info)}
    return jsonify(response)

@web_bp.route('/api/scan/report/<filename>', methods=['GET'])
def get_report(filename):
    return send_from_directory(Config.REPORTS_DIR, filename)
