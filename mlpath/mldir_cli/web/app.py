from flask import Flask, render_template, request, Response
from utils import get_json_paths
import json
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_page():
    project_name = os.path.basename(os.path.dirname(os.getcwd()))
    json_paths = get_json_paths(os.path.join(os.getcwd(), '..', 'Quests'))

    sidebar_data = {
        model_name: [
            quest_name for quest_name in json_paths[model_name]
        ] for model_name in list(json_paths.keys())
    }

    return render_template('index.html', project_name=project_name, sidebar_data=sidebar_data)


@app.route('/api/data/<string:model_name>/<string:quest_name>', methods=['GET'])
def get_data(model_name, quest_name):
    if model_name == 'undefined' or quest_name == 'undefined':
        return Response(status=400)

    json_paths = get_json_paths(os.path.join(os.getcwd(), '..', 'Quests'))
    data_file_path = json_paths[model_name][quest_name]['data']
    config_file_path = json_paths[model_name][quest_name]['config']

    data = {
        'config': None,
        'data': {
            'headers1': None,
            'headers2': None,
            'rows': None,
        }
    }

    with open(config_file_path) as f:
        config_data = json.load(f)

    with open(data_file_path) as f:
        raw_data = json.load(f)

    headers1 = list(config_data.keys())
    headers2 = [[subheader for subheader in config_data[header].keys() if config_data[header][subheader] == 'true'] for header in headers1]
    rows = {}

    for i, header in enumerate(headers2):
        for subheader in header:
            rows[f'{headers1[i]}.{subheader}'] = raw_data[headers1[i]][subheader]

    data['config'] = config_data
    data['data']['headers1'] = headers1
    data['data']['headers2'] = headers2
    data['data']['rows'] = rows

    return data

@app.route('/api/save-config-data/<string:model_name>/<string:quest_name>', methods=['POST'])
def save_config_data(model_name, quest_name):
    if model_name == 'undefined' or quest_name == 'undefined':
        return Response(status=400)

    data = request.get_json()

    json_paths = get_json_paths(os.path.join(os.getcwd(), '..', 'Quests'))
    data_file_path = json_paths[model_name][quest_name]['data']
    config_file_path = json_paths[model_name][quest_name]['config']

    with open(config_file_path) as f:
        config_data = json.load(f)

    config_data[data['header']][data['subheader']] = 'true' if data['checked'] else 'false'

    with open(config_file_path, 'w') as f:
        json.dump(config_data, f, indent=4)

    return Response(status=200)


if __name__ == '__main__':
    app.run(debug=True)