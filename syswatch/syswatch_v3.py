import collector
import csv
import json
import time
import os 


def exporter_csv(metriques, fichier):
    fichier_existe = os.path.isfile(fichier)

    with open(fichier, mode="a", newline="") as f:
        champs = [
            "timestamp",
            "hostname",
            "cpu_percent",
            "mem_total_gb",
            "mem_dispo_gb",
            "mem_percent"
        ]

        writer = csv.DictWriter(f, fieldnames=champs)

        if not fichier_existe:
            writer.writeheader()

        writer.writerow({
            "timestamp": metriques["timestamp"],
            "hostname": metriques["systeme"]["hostname"],
            "cpu_percent": metriques["cpu"]["utilisation"],
            "mem_total_gb": round(metriques["memoire"]["total"] / (1024 ** 3), 2),
            "mem_dispo_gb": round(metriques["memoire"]["disponible"] / (1024 ** 3), 2),
            "mem_percent": metriques["memoire"]["pourcentage"]
        })


def exporter_json(metriques, fichier):
    with open(fichier, "w") as f:
        json.dump(metriques, f, indent=2, default=str)


if __name__ == "__main__":
    donnees = collector.collecter_tout()
    exporter_csv(donnees, "syswatch.csv")
    exporter_json(donnees, "syswatch.json")
    print("Exports CSV et JSON effectués")
