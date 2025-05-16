import os
import json
from flask import Flask, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# --- CONFIGURAÇÃO DE PASTAS E ARQUIVOS ---
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS  = os.path.join(BASE_DIR, 'downloads')
TREATMENTS = os.path.join(BASE_DIR, 'TratamentosFIC2horas')  # ajuste se necessário
DATA_FILE  = os.path.join(BASE_DIR, 'data.json')
STOP_FILE  = os.path.join(BASE_DIR, 'stopped.json')

# --- FUNÇÃO QUE FILTRA NOS EXCELS NOVOS ---
def filter_excel_all():
    existing, keys = [], set()
    # carrega histórico
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, encoding='utf-8') as f:
            for line in f:
                obj = json.loads(line)
                existing.append(obj)
                keys.add(f"{obj['fic_number']}|{obj['start']}")
    # varre todos os XLSX em downloads/
    for fname in os.listdir(DOWNLOADS):
        if not fname.lower().endswith(('.xlsx', '.xls')):
            continue
        path = os.path.join(DOWNLOADS, fname)
        df = pd.read_excel(path, engine='openpyxl')
        df.columns = df.columns.str.strip().str.upper()
        df = df[df['TAGS'].astype(str) == '220']
        for _, row in df.iterrows():
            fic   = str(row['CIR NUMBER'])
            model = str(row['MODEL CODE'])
            start = datetime.utcnow().isoformat() + 'Z'
            key   = f"{fic}|{start}"
            if key in keys:
                continue
            existing.append({"fic_number": fic, "model": model, "tag": "220", "start": start})
            keys.add(key)
    # grava data.json novamente
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        for obj in existing:
            f.write(json.dumps(obj, ensure_ascii=False) + '\n')

# --- FUNÇÃO QUE MARCA FICS PARADAS PELOS PDFs ---
def scan_pdfs():
    stopped = set()
    if os.path.exists(STOP_FILE):
        stopped = set(json.load(open(STOP_FILE, encoding='utf-8')))
    if os.path.exists(TREATMENTS):
        for fname in os.listdir(TREATMENTS):
            if fname.lower().endswith('.pdf'):
                fic = os.path.splitext(fname)[0]
                stopped.add(fic)
    with open(STOP_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(stopped), f, ensure_ascii=False)

# --- ROTAS FLASK ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/fic-220')
def api_fic():
    out = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, encoding='utf-8') as f:
            for line in f:
                out.append(json.loads(line))
    return jsonify(out)

@app.route('/api/stopped')
def api_stopped():
    if os.path.exists(STOP_FILE):
        return jsonify(json.load(open(STOP_FILE, encoding='utf-8')))
    return jsonify([])

# --- INICIALIZAÇÃO DO SCHEDULER + FLASK ---
if __name__ == '__main__':
    sched = BackgroundScheduler()
    sched.add_job(filter_excel_all, 'interval', minutes=5)
    sched.add_job(scan_pdfs,       'interval', minutes=5)
    sched.start()
    # Usa a porta que o Replit (ou Heroku) define em PORT, ou 3000 por padrão
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
