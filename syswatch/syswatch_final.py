import time 
from models import SystemMetrics
from database import MetricsDatabase
import collector

def collect_metrics():
    data = collector.collecter_tout()

    return SystemMetrics(
        timestamp=data["timestamp"],
        hostname=data["systeme"]["hostname"],
        cpu_percent=data["cpu"]["utilisation"],
        memory_total=data["memoire"]["total"],
        memory_available=data["memoire"]["disponible"],
        memory_percent=data["memoire"]["pourcentage"],
        disk_usage=str(data["disques"])
    )

if __name__ == "__main__":
    db = MetricsDatabase()

    while True:
        metrics = collect_metrics()
        print(metrics)
        db.save(metrics)
        time.sleep(5)
