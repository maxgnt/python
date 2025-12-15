import collector 

def afficher_systeme(data):
    print("=== Système ===")
    print(f"OS : {data['os']}")
    print(f"Version : {data['version']}")
    print(f"Architecture : {data['architecture']}")
    print(f"Hostname : {data['hostname']}")
    print()

def octets_vers_go(octets):
    return f"{octets / (1024 ** 3):.2f} GB"

def afficher_cpu(data):
    print("=== CPU ===")
    print(f"Coeurs physiques : {data['coeurs_physiques']}")
    print(f"Coeurs logiques : {data['coeurs_logiques']}")
    print(f"Utilisation : {data['utilisation']} %")
    print()

def afficher_memoire(data):
    print("=== Mémoire ===")
    print(f"Total : {octets_vers_go(data['total'])}")
    print(f"Disponible : {octets_vers_go(data['disponible'])}")
    print(f"Utilisation : {data['pourcentage']} %")
    print()

def afficher_disques(disques):
    print("=== Disques ===")

    for disque in disques:
        print(f"{disque['point_montage']} : {disque['pourcentage']} % utilisé")

    print()

if __name__ == "__main__":
    print("=== SysWatch v2.0 ===\n")

    donnees = collector.collecter_tout()

    afficher_systeme(donnees["systeme"])
    afficher_cpu(donnees["cpu"])
    afficher_memoire(donnees["memoire"])
    afficher_disques(donnees["disques"])
