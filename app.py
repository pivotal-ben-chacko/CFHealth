import subprocess
import json
import os
from flask import Flask, render_template

app = Flask(__name__)

os.environ["OM_USERNAME"] = "admin"
os.environ["OM_TARGET"] = "opsman.skynetsystems.io"
os.environ["OM_PASSWORD"] = "changeme"
os.environ["OM_SKIP_SSL_VALIDATION"] = "true"

envs = { 0: {"name": "Skynet Systems", "status": "", "command": 'om curl -s -p "/api/v0/deployed/certificates?expires_within=24m"'},
         1: {"name": "Fiserv Cloud Foundry", "status": "text-bg-success", "command": 'om curl -s -p "/api/v0/deployed/certificates?expires_within=3m"'}}

QUERY_STATUS = 'om curl -s -p "/api/v0/deployed/certificates?expires_within=3m" |jq -r .certificates[].product_guid'
command2 = 'om curl -s -p "/api/v0/deployed/certificates?expires_within=24m"'
command3 = 'om curl -s -p "/api/v0/deployed/certificates?expires_within=3m"'

def run_command(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()

@app.route('/certs_expiring/env/<id>')
def switch_environment(id):
    data = run_command(QUERY_STATUS)
    cert_json = run_command(envs[int(id)]["command"])
    certificates = json.loads(cert_json)["certificates"]

    if data:
        envs[0]["status"] = "text-bg-danger"
    else:
        envs[0]["status"] = "text-bg-success"

    return render_template("index.html", envs=envs, certificates=certificates)

@app.route('/')
def index():
    data = run_command(QUERY_STATUS)
    cert_json = run_command(str(envs[0]["command"]))
    certificates = json.loads(cert_json)["certificates"]

    if data:
        envs[0]["status"] = "text-bg-danger"
    else:
        envs[0]["status"] = "text-bg-success"

    return render_template("index.html", envs=envs, certificates=certificates)
