import scapy.all as scapy
import socket
import psutil
import argparse

def get_local_ip():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_proc_name(pid):

    try:
        process = psutil.Process(pid)
        return process.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return "Unknown"

def get_conn_pids():

    conn_pids = {}
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr and conn.pid:
            conn_pids[(conn.laddr.ip, conn.laddr.port)] = conn.pid
    return conn_pids

def resolve_ip(ip):

    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return ip

def is_egress(packet, local_ip):

    return packet[scapy.IP].src == local_ip and packet.haslayer(scapy.TCP)

def packet_callback(packet, local_ip, conn_pids, resolve):

    if is_egress(packet, local_ip):
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst
        src_port = packet[scapy.TCP].sport
        dst_port = packet[scapy.TCP].dport
        
        pid = conn_pids.get((src_ip, src_port))
        process = get_proc_name(pid) if pid else "(unknown process)"
        
        try:
            service = socket.getservbyport(dst_port)
        except OSError:
            service = 'unknown'
        
        if resolve:
            dst_ip = resolve_ip(dst_ip)
        
        print(f"outbound TCP: {src_ip}:{src_port} -> {dst_ip}:{dst_port} ({service}) by {process}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--resolve", help="resolve IP addresses to hostnames", action="store_true")
    args = parser.parse_args()

    local_ip = get_local_ip()
    interface = scapy.conf.iface
    print(f"using interface: {interface} and local IP: {local_ip}")
    print("started.... press CTRL+C to stop.")

    try:
        while True:
            conn_pids = get_conn_pids() 
            scapy.sniff(iface=interface, filter="tcp", prn=lambda x: packet_callback(x, local_ip, conn_pids, args.resolve), store=False, timeout=10)
    except KeyboardInterrupt:
        print("stopped.")
        exit(0)

if __name__ == "__main__":
    main()
