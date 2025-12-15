import platform
import psutil
import socket
from datetime import datetime


def collecter_info_systeme():
    return {
        "os": platform.system(),
        "version": platform.version(),
        "architecture": platform.machine(),
        "hostname": socket.gethostname()
    }


def collecter_cpu():
    return {
        "coeurs_physiques": psutil.cpu_count(logical=False),
        "coeurs_logiques": psutil.cpu_count(logical=True),
        "utilisation": psutil.cpu_percent(interval=1)
    }


def collecter_memoire():
    memoire = psutil.virtual_memory()
    return {
        "total": memoire.total,
        "disponible": memoire.available,
        "pourcentage": memoire.percent
    }


def collecter_disques():
    disques = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disques.append({
                "point_montage": partition.mountpoint,
                "total": usage.total,
                "utilise": usage.used,
                "pourcentage": usage.percent
            })
        except PermissionError:
            continue
    return disques


def collecter_tout():
    return {
        "timestamp": datetime.now(),
        "systeme": collecter_info_systeme(),
        "cpu": collecter_cpu(),
        "memoire": collecter_memoire(),
        "disques": collecter_disques()
    }
