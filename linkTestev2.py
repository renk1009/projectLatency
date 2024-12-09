import platform
import subprocess
import time
import re

def myping(host):
    # Determina o comando de acordo com o sistema operacional
    param = ["-n", "1"] if platform.system().lower() == "windows" else ["-c", "1"]
    
    try:
        # Executa o ping e captura a saída
        result = subprocess.run(["ping"] + param + [host], stdout=subprocess.PIPE, text=True)
        
        # Verifica o código de retorno (0 = sucesso)
        if result.returncode == 0:
            # Extrai a latência usando regex
            latency = extract_latency(result.stdout)
            return True, latency
        else:
            return False, latency
    except Exception as e:
        print(f"Erro ao tentar pingar {host}: {e}")
        return False, None

def extract_latency(output):
    # Regex para capturar o tempo de resposta
    if platform.system().lower() == "windows":
        match = re.search(r"tempo[=<]\s*(\d+)ms", output, re.IGNORECASE)  # Para Windows
    else:
        match = re.search(r"time=(\d+\.\d+)\s*ms", output)  # Para Linux/Unix

    if match:
        return float(match.group(1))  # Retorna o valor da latência como número
    return None


def log_event(message):
    """Registra os eventos em um arquivo de log."""
    with open("latency_log.txt", "a") as log_file:
        log_file.write(message + "\n")

# Configurações
host = "8.8.8.8"
interval = 5  # intervalo de 5 segundos entre as verificações
latency_threshold = 70  # Limite de latência em ms

print(f"Iniciando o monitoramento. Para interromper pressione Ctrl+C.")


try:
    while True:
        is_alive, latency = myping(host)
        if is_alive:
            if latency is not None:  # Verifica se a latência foi extraída com sucesso
                if latency > latency_threshold:
                    message = f"{time.ctime()} - Host {host} está ativo, mas com latência alta: {latency} ms (Limite: {latency_threshold} ms)"
                    print(message)
                    log_event(message)  # Registra no log
                else:
                    print(f"{time.ctime()} - Host {host} está ativo - Latência: {latency} ms")
            else:
                print(f"{time.ctime()} - Host {host} está ativo, mas a latência não pôde ser determinada.")
        else:
            message = f"{time.ctime()} - Host {host} não está ativo"
            print(message)
            log_event(message)  # Registra a falha no log
        
        time.sleep(interval)
except KeyboardInterrupt:
    print("\nMonitoramento interrompido manualmente.")
