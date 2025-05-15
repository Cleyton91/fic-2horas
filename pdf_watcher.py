import os, time, json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ****************************************************
# Cole aqui o caminho exato que apareceu na barra de endereço do Explorer
SHAREPOINT_FOLDER = r"C:\Users\lb09880\OneDrive - Alliance\6 REACT\CVP\Re-ACT CVP\Tratamentos\Tratamentos FIC 2 horas"
# ****************************************************

STOP_FILE = "stopped.json"
if os.path.exists(STOP_FILE):
    stopped = set(json.load(open(STOP_FILE,encoding='utf-8')))
else:
    stopped = set()

def save():
    with open(STOP_FILE,'w',encoding='utf-8') as f:
        json.dump(list(stopped), f, ensure_ascii=False, indent=2)

class PDFHandler(FileSystemEventHandler):
    def on_created(self, e): self.handle(e.src_path, "criado")
    def on_moved(self,  e): self.handle(e.dest_path,"movido")
    def on_modified(self,e): self.handle(e.src_path, "modificado")

    def handle(self, path, action):
        if not path.lower().endswith('.pdf'):
            return
        fic = os.path.splitext(os.path.basename(path))[0]
        print(f"[{action.upper()}] {fic}")
        if fic not in stopped:
            stopped.add(fic)
            save()
            print(f"→ FIC {fic} parada!")

if __name__=='__main__':
    if not os.path.isdir(SHAREPOINT_FOLDER):
        print("ERRO: pasta não encontrada:", SHAREPOINT_FOLDER)
        exit(1)
    print("PDF watcher ativo em:", SHAREPOINT_FOLDER)
    obs = Observer()
    obs.schedule(PDFHandler(), path=SHAREPOINT_FOLDER, recursive=False)
    obs.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
    obs.join()
