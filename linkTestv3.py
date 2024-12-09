import platform
import subprocess
import time
import re
import tkinter as tk
from tkinter import messagebox

# Função de ping
def myping(host):
    param = ["-n", "1"] if platform.system().lower() == "windows" else ["-c", "1"]

    try:
        result = subprocess.run(["ping"] + param + [host], stdout=subprocess.PIPE, text=True)

        if result.returncode == 0:
            latency = extract_latency(result.stdout)
            return True, latency
        else:
            return False, None
    except Exception as e:
        print(f"Erro ao tentar pingar {host}: {e}")
        return False, None

# Função para extrair latência
def extract_latency(output):
    if platform.system().lower() == "windows":
        match = re.search(r"tempo[=<]\s*(\d+)ms", output, re.IGNORECASE)  # Para Windows
    else:
        match = re.search(r"time=(\d+\.\d+)\s*ms", output)  # Para Linux/Unix

    if match:
        return float(match.group(1))
    return None

# Função para atualizar a interface
def update_status():
    is_alive, latency = myping(host)
    
    if is_alive:
        if latency is not None:
            latency_label.config(text=f"Latência: {latency} ms")
            if latency > latency_threshold:
                log_event(f"{time.ctime()} - Latência alta: {latency} ms")
                status_label.config(text="Host ativo, mas com latência alta", fg="red")
            else:
                status_label.config(text="Host ativo - Latência dentro do limite", fg="green")
        else:
            latency_label.config(text="Latência: Não disponível")
            status_label.config(text="Host ativo - Latência não determinada", fg="orange")
    else:
        status_label.config(text="Host inativo", fg="red")
        latency_label.config(text="Latência: N/A")
        log_event(f"{time.ctime()} - Host {host} não está ativo")
    
    # Reexecuta a função após o intervalo
    root.after(interval * 1000, update_status)

# Função de log
def log_event(message):
    with open("latency_log.txt", "a") as log_file:
        log_file.write(message + "\n")

# Configurações
host = "8.8.8.8"
interval = 5  # intervalo de 5 segundos entre as verificações
latency_threshold = 70  # Limite de latência em ms

# Configura a interface gráfica
root = tk.Tk()
root.title("Monitoramento de Ping")

# Labels para mostrar o status e latência
status_label = tk.Label(root, text="Iniciando monitoramento...", font=("Arial", 14))
status_label.pack(pady=20)

latency_label = tk.Label(root, text="Latência: N/A", font=("Arial", 14))
latency_label.pack(pady=10)

# Inicia a atualização do status
update_status()

# Função para sair do programa
def on_exit():
    if messagebox.askokcancel("Sair", "Você realmente deseja sair?"):
        root.quit()

root.protocol("WM_DELETE_WINDOW", on_exit)

# Inicia o loop principal da interface gráfica
root.mainloop()
