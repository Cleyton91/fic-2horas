from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/fic-220')
def api_fic220():
    items = []
    try:
        with open('data.json','r',encoding='utf-8') as f:
            for line in f:
                items.append(json.loads(line))
    except FileNotFoundError:
        pass
    return jsonify(items)

@app.route('/api/stopped')
def api_stopped():
    try:
        with open('stopped.json','r',encoding='utf-8') as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify([])

if __name__=='__main__':
    app.run(debug=True)
