from flask import Blueprint, Response

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

metrics = Blueprint('metrics', __name__)

@metrics.route('/metrics')

def metrics_view():

    return Response(generate_latest(), mimetype = CONTENT_TYPE_LATEST)
