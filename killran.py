import os, random, string, time, psutil, subprocess, arquivos as arq, threading
import tkinter as tk
from collections import deque
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
def triple():
    TIME_WINDOW = timedelta(seconds=1)
    CHANGE_THRESHOLD = 5
    recent_changes = deque()
def create_random_file():
    filename = ''.join(random.choices(string.ascii_lowercase, k=10)) + '.txt'
    filepath = os.path.join(arq.paths['documents'], filename)
    with open(filepath, 'w') as f:
        f.write('Este é um arquivo honeypot.')
class MyHandler(FileSystemEventHandler):
    def __init__(self, text_widget):
        self.text_widget = text_widget
    def on_modified(self, event):
        if event.is_directory:
            return None
        else:
            filename = os.path.basename(event.src_path)
            for path in arq.paths.values():
                specified_filename = os.path.basename(path)
                if filename.startswith(specified_filename):
                    message = f"Arquivo alterado: {event.src_path}"
                    self.log_event(message)
                    self.update_gui(message)
                    matar()
    def on_deleted(self, event):
        if event.is_directory:
            return None
        elif event.src_path in arq.paths.values():
            message = f"Arquivo excluído: {event.src_path}"
            self.log_event(message)
            self.update_gui(message)
            matar()
    def on_created(self, event):
        if event.is_directory:
            return None
        else:
            filename = os.path.basename(event.src_path)
            for path in arq.paths.values():
                specified_filename = os.path.basename(path)
                if filename.startswith(specified_filename):
                    message = f"Arquivo criado: {event.src_path}"
                    self.log_event(message)
                    self.update_gui(message)
                    matar()
    def log_event(self, message):
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(arq.log.log_file_path, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")
    def update_gui(self, message):
        self.text_widget.after(0, self.text_widget.insert, tk.END, message + '\n')
class ObserverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor de Eventos")
        self.text_widget = tk.Text(root, wrap=tk.WORD, height=10, width=40)
        self.text_widget.pack()
        self.start_button = tk.Button(root, text="Iniciar Monitor", command=self.start_observer)
        self.start_button.pack()
        self.stop_button = tk.Button(root, text="Parar Monitoramento", command=self.stop_observer)
        self.stop_button.pack()
        self.observer = None
    def start_observer(self):
        def target():
            event_handler = MyHandler(self.text_widget)
            self.observer = Observer()
            for path in arq.paths.values():
                if os.path.exists(path):
                    print(f"marcando analizador para o caminho: {path}")  
                    self.observer.schedule(event_handler, path, recursive=False)
                else:
                    print(f"O diretório {path} não existe.")
            
            
            self.create_honeypots()  
            print("Iniciando o log...")  
            self.observer.start()
            try:
                while True:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                self.observer.stop        
            self.observer.join()

        threading.Thread(target=target).start()

    def stop_observer(self):
        if self.observer:
            print("Parando observador...")  
            self.observer.stop()
            
        self.delete_honeypots() 

    def create_random_file(self):
        filename = ''.join(random.choices(string.ascii_lowercase, k=10)) + '.txt'
        filepath = os.path.join(arq.paths['documents'], filename)
        with open(filepath, 'w') as f:
            f.write('Este é um arquivo honeypot.')

    def create_honeypots(self):
        num_honeypots = 5  
        for _ in range(num_honeypots):
            self.create_random_file()
    def delete_honeypots(self):
        for filename in os.listdir(arq.documents_path):
            filepath = os.path.join(arq.documents_path, filename)
            if os.path.isfile(filepath) and filename.endswith('.txt'):
                os.remove(filepath)
def update_gui(self, message):
    print(f"Atualizando a interface gráfica com a mensagem: {message}")  
    self.text_widget.after(0, self.text_widget.insert, tk.END, message + '\n')
def is_legitimate(process):
    try:
        exe_path = process.info['exe']
        if exe_path != None and not exe_path.startswith("C:\\Windows") and process.info['name'] not in ["System", "Registry", "python.exe", "Catcher.exe"]:
           
            return False
        return True
    except Exception as e:
        print("Erro não previsto:", e)
        return False
def taskkill(pid):
    try:
        subprocess.call(["taskkill", "/F", "/PID", str(pid)])
    except Exception as e:
        print(f"Erro ao tentar matar o processo {pid}: {e}")

def matar():
    proc_mal_pids = set()
    try: 
        for process in psutil.process_iter(["name", "pid", "exe"]):
            legit = is_legitimate(process)
            if not legit:
                proc_mal_pids.add(process.pid)
            else:
                continue
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    for proc in proc_mal_pids:
        print(proc)
        taskkill(proc)
