import os
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)
from datetime import datetime

app = Flask(__name__)

# =============================================================================
# HEALTH CHECK ENDPOINTS (Required for CI/CD)
# These endpoints are used by the pipeline to verify deployments
# =============================================================================

@app.route('/health')
def health_check():
    """
    Health check endpoint - Used by CI/CD pipeline to verify app is running.
    Returns: JSON with status, timestamp, environment, and version.
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv("FLASK_ENV", "development"),
        "version": os.getenv("APP_VERSION", "1.0.0")
    })

@app.route('/ready')
def readiness_check():
    """
    Readiness check - Indicates if app is ready to receive traffic.
    Used after deployment to confirm the app is fully operational.
    """
    return jsonify({
        "ready": True,
        "environment": os.getenv("FLASK_ENV", "development")
    })

# =============================================================================
# ORIGINAL APPLICATION ROUTES
# =============================================================================

@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))

# =============================================================================
# API ENDPOINTS (For demonstrating tests)
# =============================================================================

@app.route('/api/greet/<name>')
def api_greet(name):
    """API endpoint for greeting - easy to test."""
    return jsonify({
        "message": f"Hello, {name}!",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/add', methods=['POST'])
def api_add():
    """Simple calculator endpoint for unit test demonstration."""
    data = request.get_json() or {}
    a = data.get('a', 0)
    b = data.get('b', 0)
    return jsonify({"result": a + b})


if __name__ == '__main__':
    port = int(os.getenv("PORT", 9000))
    debug = os.getenv("FLASK_ENV") == "development"
    app.run(host='0.0.0.0', port=port, debug=debug)
