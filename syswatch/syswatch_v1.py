import platform
import psutil


def afficher_infos_systeme(): 
    print ("=== Système ===")
    print (f"OS: {platform.system()}")
    print (f"Version: {platform.version()}")
    print (f"Architecture: {platform.machine()}")
    print (f"Hostname: {socket.gethostname()}")
    print (f"Python : {sys.version.split()[0]}")
    print()

def afficher_cpu():
    print("=== CPU ===")
    print(f"Coeurs physiques : {psutil.cpu_count(logical=False)}")
    print(f"Coeurs logiques : {psutil.cpu_count(logical=True)}")
    print(f"Utilisation : {psutil.cpu_percent(interval=1)} %")
    print()

def afficher_memoire():
    memoire = psutil.virtual_memory()

    total_go = memoire.total / (1024 ** 3)
    dispo_go = memoire.available / (1024 ** 3)

    print("=== Mémoire ===")
    print(f"Total : {total_go:.2f} GB")
    print(f"Disponible : {dispo_go:.2f} GB")
    print(f"Utilisation : {memoire.percent} %")
    print()

def afficher_disques():
    print("=== Disques ===")

    partitions = psutil.disk_partitions()

    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"{partition.mountpoint} : {usage.percent} % utilisé")
        except PermissionError:
            print(f"{partition.mountpoint} : permission refusée")

    print()

if __name__ == "__main__":
    print("=== SysWatch v1.0 ===\n")

    afficher_infos_systeme()
    afficher_cpu()
    afficher_memoire()
    afficher_disques()
