# Meshtastic CLI Setup Guide for WSL2

## Overview

This guide provides step-by-step instructions for configuring Ubuntu on WSL2 to access Meshtastic radios via USB and installing the Meshtastic standalone CLI tool.

## Prerequisites

- Windows 10/11 with WSL2 installed
- Ubuntu distribution running on WSL2
- Administrative access to Windows
- Meshtastic-compatible radio device (e.g., Heltec, RAK, LILYGO)

## Architecture

The setup involves three main components:

1. **Windows USB/IP daemon** (`usbipd-win`) - Shares USB devices from Windows to WSL2
2. **WSL2 USB/IP client** - Attaches shared USB devices to the Linux environment
3. **Meshtastic CLI** - Python-based command-line interface for radio communication

## Part 1: Windows Configuration

### Install usbipd-win

1. Download the latest release from the official repository:
   ```
   https://github.com/dorssel/usbipd-win/releases
   ```

2. Install the MSI package with administrative privileges

3. Verify installation by opening PowerShell (as Administrator) and running:
   ```powershell
   usbipd --version
   ```

### Attach Meshtastic Device to WSL2

1. Connect your Meshtastic radio via USB

2. List available USB devices (PowerShell as Administrator):
   ```powershell
   usbipd list
   ```

3. Identify your Meshtastic device. Common identifiers:
   - **ESP32-based devices**: Espressif, Heltec, LILYGO
   - **nRF52-based devices**: RAK Wireless

4. Bind the device (one-time setup, replace `<BUSID>` with actual bus ID):
   ```powershell
   usbipd bind --busid <BUSID>
   ```

5. Attach the device to WSL2:
   ```powershell
   usbipd attach --wsl --busid <BUSID>
   ```

6. To automatically attach on connection, use the `--auto-attach` flag:
   ```powershell
   usbipd attach --wsl --busid <BUSID> --auto-attach
   ```

**Note**: The device must be re-attached after each Windows reboot or device reconnection (unless auto-attach is configured).

## Part 2: WSL2 Configuration

### Install System Dependencies

Update package repositories and install required packages:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv usbutils
```

### Configure USB Device Permissions

1. Create udev rules for Meshtastic devices:

```bash
sudo tee /etc/udev/rules.d/99-meshtastic.rules << 'EOF'
# Meshtastic USB devices - ESP32
SUBSYSTEM=="tty", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", MODE="0666", GROUP="dialout"
SUBSYSTEM=="usb", ATTRS{idVendor}=="303a", ATTRS{idProduct}=="1001", MODE="0666", GROUP="dialout"

# Common USB-Serial adapters (CP210x, CH340)
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", MODE="0666", GROUP="dialout"
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE="0666", GROUP="dialout"

# FTDI adapters
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", MODE="0666", GROUP="dialout"
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6015", MODE="0666", GROUP="dialout"
EOF
```

2. Add your user to the `dialout` group:

```bash
sudo usermod -a -G dialout $USER
```

3. Reload udev rules:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

4. Apply group membership (choose one):
   - **Option A**: Log out and back in to WSL2
   - **Option B**: Run `newgrp dialout` in current session
   - **Option C**: Close and reopen terminal

### Install Meshtastic CLI

#### Option 1: Install via pip (Recommended)

```bash
pip3 install --user meshtastic
```

Add Python user bin directory to PATH (add to `~/.bashrc` or `~/.zshrc`):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Reload shell configuration:

```bash
source ~/.bashrc
```

#### Option 2: Install Standalone Binary

1. Download the standalone CLI:

```bash
wget https://github.com/meshtastic/python/releases/latest/download/meshtastic-linux-x86_64 \
  -O ~/meshtastic
```

2. Make executable:

```bash
chmod +x ~/meshtastic
```

3. (Optional) Create symlink for system-wide access:

```bash
sudo ln -s ~/meshtastic /usr/local/bin/meshtastic
```

## Part 3: Verification

### Verify USB Connection

Check if device is attached to WSL2:

```bash
lsusb
```

Expected output (example for Heltec V4):
```
Bus 001 Device 002: ID 303a:1001 Espressif heltec_wifi_lora_32 v4
```

Check serial device availability:

```bash
ls -l /dev/ttyACM* /dev/ttyUSB*
```

Expected output:
```
crw-rw-rw- 1 root dialout 166, 0 Jan 11 06:08 /dev/ttyACM0
```

### Test Meshtastic Connection

Connect to the radio and retrieve device information:

```bash
meshtastic --info
```

Expected output should include:
- Connection confirmation
- Device owner and node information
- Firmware version and hardware model
- Node database with visible mesh nodes
- Device preferences and module configurations
- Channel information

### Common Serial Devices

Different Meshtastic hardware uses different serial interfaces:

| Hardware | Serial Device | Chipset |
|----------|--------------|---------|
| Heltec (V3, V4, Wireless Tracker) | `/dev/ttyACM0` | ESP32 |
| LILYGO T-Beam, T-Echo | `/dev/ttyACM0` or `/dev/ttyUSB0` | ESP32 or nRF52 |
| RAK WisBlock (RAK4631) | `/dev/ttyACM0` | nRF52840 |
| Station G1, G2 | `/dev/ttyUSB0` | ESP32 with CP210x |

## Part 4: Usage

### Basic Commands

```bash
# Display device information
meshtastic --info

# List nodes in mesh
meshtastic --nodes

# Send message to all nodes
meshtastic --sendtext "Hello mesh!" --dest ^all

# Send direct message to specific node
meshtastic --sendtext "Private message" --dest '!6984a7c8'

# Get device configuration
meshtastic --get-config

# Set device owner
meshtastic --set-owner "Your Name" --set-owner-short "NAME"

# Set LoRa region
meshtastic --set lora.region US

# Export channel configuration as URL
meshtastic --info | grep "Complete URL"

# Monitor incoming messages
meshtastic --listen
```

### Advanced Operations

```bash
# Backup device configuration
meshtastic --export-config > meshtastic-backup.yaml

# Restore configuration
meshtastic --configure meshtastic-backup.yaml

# Update firmware (use with caution)
meshtastic --flash-esp32 firmware-file.bin

# Factory reset device
meshtastic --factory-reset

# Reboot device
meshtastic --reboot

# Specify custom serial port
meshtastic --port /dev/ttyUSB0 --info
```

## Troubleshooting

### Device Not Found

**Symptoms**: `meshtastic` cannot connect to device

**Solutions**:

1. Verify USB device is attached in Windows:
   ```powershell
   usbipd list
   ```

2. Re-attach device:
   ```powershell
   usbipd attach --wsl --busid <BUSID>
   ```

3. Check device visibility in WSL2:
   ```bash
   lsusb
   dmesg | grep -i tty | tail -10
   ```

4. Verify permissions:
   ```bash
   ls -l /dev/ttyACM0
   groups  # Should include 'dialout'
   ```

### Permission Denied

**Symptoms**: `Permission denied: '/dev/ttyACM0'`

**Solutions**:

1. Verify dialout group membership:
   ```bash
   groups
   ```

2. If not in dialout group, add user:
   ```bash
   sudo usermod -a -G dialout $USER
   ```

3. Apply changes:
   ```bash
   newgrp dialout
   # or log out and back in
   ```

4. Check device permissions:
   ```bash
   ls -l /dev/ttyACM0
   # Should show: crw-rw-rw- 1 root dialout
   ```

### Multiple Serial Devices

**Symptoms**: Multiple `/dev/ttyACM*` or `/dev/ttyUSB*` devices present

**Solutions**:

1. List all serial devices with details:
   ```bash
   ls -l /dev/serial/by-id/
   ```

2. Specify device explicitly:
   ```bash
   meshtastic --port /dev/ttyACM1 --info
   ```

3. Use device by-id path for consistency:
   ```bash
   meshtastic --port /dev/serial/by-id/usb-Heltec_... --info
   ```

### Connection Timeout

**Symptoms**: "Timed out waiting for connection"

**Solutions**:

1. Ensure device is not in use by another application
2. Try resetting the device (power cycle or reset button)
3. Increase timeout:
   ```bash
   meshtastic --info --timeout 60
   ```
4. Check for kernel driver issues:
   ```bash
   dmesg | tail -20
   ```

### WSL2 USB Not Working After Windows Update

**Solutions**:

1. Reinstall usbipd-win on Windows
2. Rebuild WSL2 USB support:
   ```bash
   sudo apt install --reinstall linux-tools-generic hwdata
   ```
3. Restart WSL2:
   ```powershell
   wsl --shutdown
   wsl
   ```

## Security Considerations

### Device Access Control

- The `MODE="0666"` in udev rules allows any user to access the device
- For stricter security, use `MODE="0660"` (dialout group only)
- Consider using `admin_key` in Meshtastic for device configuration protection

### Bluetooth Security

If using Bluetooth instead of USB:

```bash
meshtastic --ble "DeviceName" --info
```

Configure PIN mode:
```bash
meshtastic --set bluetooth.mode FIXED_PIN
meshtastic --set bluetooth.fixed_pin 123456
```

## Additional Resources

- **Official Documentation**: https://meshtastic.org/docs/software/python/cli/
- **GitHub Repository**: https://github.com/meshtastic/python
- **Community Forum**: https://meshtastic.discourse.group/
- **Discord**: https://discord.gg/meshtastic
- **usbipd-win Project**: https://github.com/dorssel/usbipd-win

## Appendix A: Common Vendor/Product IDs

| Device | Vendor ID | Product ID |
|--------|-----------|------------|
| ESP32 (Generic) | 303a | 1001 |
| CP210x (Silicon Labs) | 10c4 | ea60 |
| CH340 (WCH) | 1a86 | 7523 |
| FTDI FT232 | 0403 | 6001 |
| FTDI FT231X | 0403 | 6015 |
| Nordic nRF52 | 1915 | 521f |

## Appendix B: Automation Scripts

### Auto-attach USB Device (PowerShell)

Save as `attach-meshtastic.ps1`:

```powershell
# Replace with your device's bus ID
$BUSID = "1-1"

# Check if device is already attached
$attached = usbipd list | Select-String -Pattern "$BUSID.*Attached"

if (-not $attached) {
    Write-Host "Attaching Meshtastic device..."
    usbipd attach --wsl --busid $BUSID
} else {
    Write-Host "Device already attached."
}
```

### Quick Connection Test (Bash)

Save as `~/bin/mesh-test.sh`:

```bash
#!/bin/bash

if meshtastic --info --timeout 10 &> /dev/null; then
    echo "✓ Meshtastic device connected"
    exit 0
else
    echo "✗ Cannot connect to Meshtastic device"
    echo "  Check USB attachment and permissions"
    exit 1
fi
```

Make executable:
```bash
chmod +x ~/bin/mesh-test.sh
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-11 | Initial documentation |

---

*Document maintained for Meshtastic CLI version 2.7.x on WSL2/Ubuntu*
