# PyBluezJammer
A Python-based Bluetooth disruption tool leveraging built-in Bluetooth adapters on Kali Linux/Nethunter.

# PyBluezJammer

A Bluetooth disruption tool for Kali Linux/Nethunter using built-in adapters.

## Features
- Scan for nearby Bluetooth devices
- Flood target devices with L2CAP pings
- Multi-worker process support

## Requirements
- Kali Linux/Nethunter
  `pip install colorama`
- `bluez` tools (install with `sudo apt install bluez`)

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/Spiderssh/PyBluezJammer.git
   cd PyBluezJammer
    ```
 2. Run the tool:
   ```bash
   sudo python3 bluetooth_jammer.py
   ```
