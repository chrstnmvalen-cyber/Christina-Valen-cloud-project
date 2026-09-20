from flask import Flask, request, jsonify

import requests

load_balancer = Flask(__name__)

targets = ["http://0.0.0.0:5001/", "http://0.0.0.0:5002","http://0.0.0.0:5003","http://0.0.0.0:5004"]

index = 0

@load_balancer.route("/<path:path>", methods=["GET", "POST"])

def balance(path):

    global index

    target = targets[index]

    index = (index + 1) % len(targets)  # Round-robin distribution

    url = f"{target}/{path}"

    resp = requests.request(method=request.method, url=url, data=request.data, headers=request.headers)

    return (resp.content, resp.status_code, resp.headers.items())

if __name__ == "__main__":

    load_balancer.run(host='0.0.0.0', port=8000)
