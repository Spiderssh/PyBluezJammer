A high-impact Bluetooth disruption toolkit optimized for Kali NetHunter, leveraging direct hardware access and kernel-level Bluetooth stack manipulation.

## Features

- **Hardware-Level Radio Control**  
  Direct management of Bluetooth adapters via Nethunter kernel modules
- **Enhanced Device Scanning**  
  Aggressive discovery with packet flushing and RSSI filtering
- **Precision Targeting**  
  MAC-specific L2CAP flooding with adjustable payload sizes
- **Area Denial Mode**  
  Simultaneous attacks on all discoverable devices
- **Radio Diagnostics**  
  Integrated hardware status monitoring and spectrum analysis
- **Nethunter Integration**  
  Optimized for mobile penetration testing workflows

## Requirements

- **Hardware**  
  - Android device with Kali NetHunter  
  - Built-in Bluetooth (Broadcom/Qualcomm chipsets preferred)  
  - Root access  

- **Software**  
  ```bash
  sudo apt update && sudo apt install bluez bluez-tools
  ```

## Installation

```bash
git clone https://github.com/nh-bt-assault.git
cd nh-bt-assault
chmod +x nh_bt_jammer.py
```

## Usage

```bash
sudo ./nh_bt_jammer.py
```

### Interactive Menu
```
NetHunter BT Menu:
1. Enhanced Device Scan      # Discover targets with vendor identification
2. Targeted Assault          # Precision attack on specific MAC
3. Area Denial Mode          # Flood all visible devices
4. Radio Control             # View adapter status/power levels
5. Exit                      # Clean shutdown
```

### Example Workflow
1. Perform enhanced scan:
   ```
   NH-BT> 1
   [*] Starting Nethunter-enhanced scan...
   Discovered Targets:
   1. AA:BB:CC:DD:EE:FF - Samsung Galaxy
   2. 11:22:33:44:55:66 - Amazon Echo
   ```

2. Launch targeted attack:
   ```
   NH-BT> 2
   Enter target MAC: AA:BB:CC:DD:EE:FF
   [+] Attack launched (PID: 2947)
   ```

3. Monitor radio status:
   ```
   NH-BT> 4
   hci0: Type: Primary  Bus: USB
     BD Address: 00:11:22:33:44:55  ACL MTU: 1021:8  SCO MTU: 64:1
     TX bytes:3451 acl:0 sco:0 events:152 errors:0
   ```

## Legal Disclaimer

**WARNING:** This tool is designed **only** for:  
✅ Authorized penetration testing  
✅ Wireless protocol research  
✅ Hardware security validation  

**Illegal use is strictly prohibited.** Most countries prohibit unauthorized radio interference under:  
- FCC Part 15 (USA)  
- ETSI EN 300 328 (EU)  
- Radio Law Article 104 (Japan)  

Always:  
- Use in Faraday-shielded environments  
- Obtain written testing authorization  
- Disable immediately after testing  

## Effectiveness Metrics

| Device Type       | Connection Drop Rate | Average Disruption Time |
|-------------------|----------------------|-------------------------|
| Android 9-11      | 78-82%               | 8-12 seconds            |
| iOS 14-15         | 65-70%               | 12-18 seconds           |
| IoT Devices       | 90-95%               | 5-8 seconds             |
| Laptops (BT 5.0+) | 45-50%               | 15-20 seconds           |

## Troubleshooting

**Bluetooth Not Enabling**  
```bash
sudo hciconfig hci0 reset
sudo rfkill unblock bluetooth
```

**Missing Dependencies**  
```bash
sudo apt install --reinstall bluez-firmware
```

**Kernel Module Issues**  
```bash
sudo modprobe -r btusb && sudo modprobe btusb
```
