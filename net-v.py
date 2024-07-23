import ipaddress
import sys
from colorama import Fore, Style, init

def expand_subnet(network, subnet):
    # Extraer la red base
    base_network = ipaddress.ip_network(network, strict=False)
    base_ip = str(base_network.network_address).split('.')[:3]

    # Si el subnet ya es una IP completa, devolverla tal cual
    if '/' in subnet:
        parts = subnet.split('/')
        ip_parts = parts[0].split('.')
        if len(ip_parts) == 4:
            return subnet
        elif len(ip_parts) == 2:
            # Expandir forma corta 1.1/30 a 192.168.1.1/30
            return f"{base_ip[0]}.{base_ip[1]}.{ip_parts[0]}.{ip_parts[1]}/{parts[1]}"

    raise ValueError(f"Formato de subred no válido: {subnet}")

def get_reserved_and_available_hosts(network, subnets):
    main_network = ipaddress.ip_network(network, strict=False)
    reserved_hosts = set()
    overlapping_subnets = []
    subnet_ranges = []

    for i, subnet in enumerate(subnets):
        try:
            subnet = expand_subnet(network, subnet)
            subnet_network = ipaddress.ip_network(subnet, strict=False)
            if not main_network.supernet_of(subnet_network):
                overlapping_subnets.append(f"WARNING: La subred {subnet} no está dentro de la red principal {network}")
                continue

            current_reserved = set(subnet_network.hosts())
            current_reserved.add(subnet_network.network_address)
            current_reserved.add(subnet_network.broadcast_address)

            for j, other_subnet in enumerate(subnets[:i]):
                other_subnet = expand_subnet(network, other_subnet)
                other_subnet_network = ipaddress.ip_network(other_subnet, strict=False)
                other_reserved = set(other_subnet_network.hosts())
                other_reserved.add(other_subnet_network.network_address)
                other_reserved.add(other_subnet_network.broadcast_address)
                if current_reserved.intersection(other_reserved):
                    overlapping_subnets.append(f"WARNING: Superposición detectada entre {subnet} y {other_subnet}")
                    break

            subnet_ranges.append(current_reserved)
            reserved_hosts.update(current_reserved)

        except ValueError as e:
            overlapping_subnets.append(f"WARNING: {subnet} - {str(e)}")

    reserved_hosts = sorted(reserved_hosts)
    all_hosts = sorted(set(main_network.hosts()) - set(reserved_hosts))

    reserved_segments = []
    available_segments = []

    if reserved_hosts:
        start = reserved_hosts[0]
        prev = reserved_hosts[0]
        for ip in reserved_hosts[1:]:
            if ip - 1 != prev:
                reserved_segments.append((start, prev))
                start = ip
            prev = ip
        reserved_segments.append((start, prev))

    if all_hosts:
        start = all_hosts[0]
        prev = all_hosts[0]
        for ip in all_hosts[1:]:
            if ip - 1 != prev:
                available_segments.append((start, prev))
                start = ip
            prev = ip
        available_segments.append((start, prev))

    return reserved_segments, available_segments, overlapping_subnets

def visualize_hosts(network, reserved_segments, available_segments):
    main_network = ipaddress.ip_network(network, strict=False)
    all_hosts = list(main_network.hosts())

    for host in all_hosts:
        last_octet = int(str(host).split('.')[-1])
        if any(start <= host <= end for start, end in reserved_segments):
            print(Fore.RED + f"{last_octet:3}", end=' ')
        else:
            print(Fore.GREEN + f"{last_octet:3}", end=' ')
        if last_octet % 16 == 15:
            print()
    print()

def main():
    init(autoreset=True)
    if len(sys.argv) < 3:
        print("Uso: python3 net-visualizer.py <red> <subred> <subred> ... [-v|--visualizer]")
        return

    visualize = False
    if '-v' in sys.argv or '--visualizer' in sys.argv:
        visualize = True
        sys.argv.remove('-v') if '-v' in sys.argv else sys.argv.remove('--visualizer')

    network = sys.argv[1]
    subnets = sys.argv[2:]

    reserved_segments, available_segments, warnings = get_reserved_and_available_hosts(network, subnets)

    for warning in warnings:
        print(Fore.YELLOW + warning)

    if warnings:
        print(Fore.YELLOW + "No se muestra el mapa de hosts debido a las advertencias anteriores.")
        return

    if visualize:
        visualize_hosts(network, reserved_segments, available_segments)
    else:
        print("Segmentos reservados:")
        for start, end in reserved_segments:
            print(Fore.RED + f"{start} - {end}")

        print("Disponibles:")
        for start, end in available_segments:
            print(Fore.GREEN + f"{start} - {end}")

if __name__ == "__main__":
    main()
