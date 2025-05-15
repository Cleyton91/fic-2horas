import os, sys, json
from datetime import datetime
import pandas as pd

DATA_FILE = "data.json"

# 1) Carrega o histórico existente (se houver)
existing = []
if os.path.exists(DATA_FILE):
    with open(DATA_FILE,'r',encoding='utf-8') as f:
        for line in f:
            try: existing.append(json.loads(line))
            except: pass
existing_keys = {item['fic_number']+'|'+item['start'] for item in existing}

# 2) Recebe o Excel como argumento
if len(sys.argv)<2:
    print("Uso: python filter_excel.py <caminho_para_excel>")
    sys.exit(1)
excel_path = sys.argv[1]
if not os.path.isfile(excel_path):
    print("Arquivo não encontrado:", excel_path)
    sys.exit(1)

# 3) Lê e normaliza cabeçalhos
df = pd.read_excel(excel_path, engine='openpyxl')
df.columns = df.columns.str.strip().str.upper()

# 4) Garante que CIR NUMBER, MODEL CODE e TAGS existam
for col in ("CIR NUMBER","MODEL CODE","TAGS"):
    if col not in df.columns:
        print("Colunas disponíveis:", df.columns.tolist())
        raise KeyError(f"Coluna obrigatória não encontrada: {col}")

# 5) Filtra só TAGS == "220"
df = df[df["TAGS"].astype(str)=="220"]

# 6) Para cada nova linha, gera um único timer
added = 0
for _,row in df.iterrows():
    fic   = str(row["CIR NUMBER"])
    model = str(row["MODEL CODE"])
    start = datetime.utcnow().isoformat()+"Z"
    key   = fic + "|" + start
    if key in existing_keys: 
        continue
    existing.append({
        "fic_number": fic,
        "model":      model,
        "tag":        "220",
        "start":      start
    })
    existing_keys.add(key)
    added += 1

# 7) Regrava tudo (histórico + novos)
with open(DATA_FILE,'w',encoding='utf-8') as out:
    for item in existing:
        out.write(json.dumps(item, ensure_ascii=False)+"\n")

print(f"✅ data.json atualizado: +{added} novos timers de {os.path.basename(excel_path)}")
