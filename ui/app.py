from flask import Flask, render_template, request, Response
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', project_name="Demo Project")


@app.route('/api/data')
def data():
    data = {
        'config': None,
        'data': {
            'headers1': None,
            'headers2': None,
            'rows': None,
        }
    }

    with open('data2-config.json') as f:
        configData = json.load(f)

    with open('data2.json') as f:
        rawData = json.load(f)

    headers1 = list(configData.keys())
    headers2 = [[subheader for subheader in configData[header].keys() if configData[header][subheader] == 'true'] for header in headers1]
    rows = {}

    for i, header in enumerate(headers2):
        for subheader in header:
            rows[f'{headers1[i]}.{subheader}'] = rawData[headers1[i]][subheader]

    data['config'] = configData
    data['data']['headers1'] = headers1
    data['data']['headers2'] = headers2
    data['data']['rows'] = rows

    return data

@app.route('/api/save-config-data', methods=['POST'])
def saveConfigData():
    data = request.get_json()

    with open('data2-config.json', 'r') as f:
        configData = json.load(f)

    configData[data['header']][data['subheader']] = 'true' if data['checked'] else 'false'

    with open('data2-config.json', 'w') as f:
        json.dump(configData, f, indent=4)

    return Response(status=200)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)