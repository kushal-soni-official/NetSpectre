from flask import Blueprint, render_template, request, jsonify, send_from_directory
from netspectre.scanner import task_manager
from netspectre.config import Config
import os
import json
import time

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    return render_template('index.html')

@web_bp.route('/api/scan/start', methods=['POST'])
def start_scan():
    data = request.json
    target = data.get('target')
    mode = data.get('mode', 'light')
    
    if not target:
        return jsonify({"error": "Target subnet is required"}), 400
        
    task_id = task_manager.submit_scan(target, mode)
    return jsonify({"task_id": task_id}), 202

@web_bp.route('/api/scan/<task_id>/status', methods=['GET'])
def get_status(task_id):
    task = task_manager.get_status(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
        
    response = {
        "state": task['state'],
        "status": task['status'],
        "elapsed": task.get('elapsed', 0),
        "duration": task.get('duration', 0)
    }
    if task['state'] == 'SUCCESS':
        response['result'] = task['result']
        
    return jsonify(response)

@web_bp.route('/api/scan/<task_id>/stop', methods=['POST'])
def stop_scan(task_id):
    success = task_manager.stop_scan(task_id)
    return jsonify({"success": success})

@web_bp.route('/api/scan/report/<filename>', methods=['GET'])
def get_report(filename):
    return send_from_directory(Config.REPORTS_DIR, filename)

# --- Stored Data & History ---
@web_bp.route('/api/history', methods=['GET'])
def get_history():
    # List reports in the reports directory
    reports = []
    if os.path.exists(Config.REPORTS_DIR):
        for f in os.listdir(Config.REPORTS_DIR):
            if f.endswith('.html'):
                reports.append({
                    "filename": f,
                    "date": time.ctime(os.path.getmtime(os.path.join(Config.REPORTS_DIR, f)))
                })
    return jsonify({"reports": sorted(reports, key=lambda x: x['date'], reverse=True)})
