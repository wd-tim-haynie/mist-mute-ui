from flask import Flask, render_template, jsonify, request
from mist_mute import get_sites, get_active_mutes, add_mute
from pprint import pprint
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get-sites', methods=['GET'])
def get_sites_route():
    sites = get_sites()
    return jsonify(sites)


@app.route("/get-active-mutes")
def get_active_mutes_route():
    active_mutes = get_active_mutes()
    sites = get_sites()

    site_id_to_name = {site["id"]: site["name"] for site in sites}

    for mute in active_mutes:
        mute["site_name"] = site_id_to_name.get(mute["site_id"])

    return jsonify(active_mutes)


@app.route('/add-mute', methods=['POST'])
def add_mute_route():
    id = request.json.get('id')
    start_time = request.json.get('start_time')

    # Set start_time to current time if not provided
    if not start_time:
        start_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    duration = request.json.get('duration')
    duration = int(duration) * 3600 if duration else 3600  # Convert hours to seconds or use 1 hour as default
    add_mute(id, start_time, duration)
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run(debug=True)
