# Meshtastic Scripts

A collection of powerful automation and monitoring scripts for Meshtastic mesh radio networks.

## Overview

These scripts provide advanced capabilities for managing, monitoring, and automating Meshtastic mesh networks using the Python CLI.

## Scripts

### 1. 📊 Mesh Monitor (`mesh-monitor.py`)

Real-time dashboard showing all mesh nodes with SNR, battery levels, and activity.

**Usage:**
```bash
./mesh-monitor.py
./mesh-monitor.py --port /dev/ttyACM0
```

**Features:**
- Live node count and statistics
- SNR signal quality indicators
- Battery level monitoring
- Hop count display
- Auto-refresh every 30 seconds
- Color-coded signal quality

### 2. 📝 Message Logger (`message-logger.py`)

Logs all mesh messages to timestamped files for archival and analysis.

**Usage:**
```bash
./message-logger.py
./message-logger.py --port /dev/ttyACM0
./message-logger.py --logfile custom-log.txt
```

**Features:**
- Timestamps all messages
- Logs sender, receiver, and message content
- Records telemetry and system events
- Automatically creates daily log files
- Console + file output

### 3. 🚨 Emergency Broadcast (`emergency-broadcast.sh`)

Send urgent messages to all mesh nodes with confirmation prompts.

**Usage:**
```bash
./emergency-broadcast.sh "Meeting at 1500h"
./emergency-broadcast.sh --urgent "Emergency alert"
./emergency-broadcast.sh --ack --port /dev/ttyACM0 "Important message"
```

**Features:**
- Confirmation prompt before sending
- Optional URGENT prefix
- Acknowledgment support
- Color-coded output

### 4. 📡 Mesh Roll Call (`mesh-rollcall.sh`)

Poll all known nodes to check which are online and responsive.

**Usage:**
```bash
./mesh-rollcall.sh
./mesh-rollcall.sh --port /dev/ttyACM0
```

**Features:**
- Requests telemetry from all nodes
- Reports response/no-response status
- Calculates response rate
- Shows node names and IDs
- Color-coded results

### 5. 💾 Backup All Radios (`backup-all-radios.sh`)

Automatically backup configurations from all connected Meshtastic devices.

**Usage:**
```bash
./backup-all-radios.sh
```

**Features:**
- Auto-detects all connected radios
- Creates timestamped backups
- Uses friendly node names in filenames
- Saves to `~/meshtastic-backups/`
- Reports success/failure for each device

### 6. 🏥 Node Health Alerter (`node-health-alert.py`)

Monitor critical nodes for offline status, low battery, or poor signal quality.

**Usage:**
```bash
./node-health-alert.py --nodes !6984a7c8 !b2a70de4
./node-health-alert.py --nodes !6984a7c8 --interval 600 --battery-threshold 25
./node-health-alert.py --port /dev/ttyACM0 --nodes !6984a7c8 !b2a70de4
```

**Features:**
- Monitors specific critical nodes
- Battery level alerts (default: <20%)
- Signal quality warnings (SNR < -10dB)
- Offline detection
- Configurable check interval
- Rate limiting (max 1 alert/hour per issue)

## Requirements

- Meshtastic CLI (standalone or via pip)
- Python 3.6+ (for Python scripts)
- Bash (for shell scripts)
- Linux/WSL2/macOS environment

## Installation

1. Clone this repository:
```bash
cd ~/repos
git clone <your-repo-url> meshtastic-scripts
cd meshtastic-scripts
```

2. Ensure scripts are executable:
```bash
chmod +x *.sh *.py
```

3. Update `MESHTASTIC_CMD` path in scripts if needed:
   - Default: `meshtastic` (assumes in PATH)
   - Or: `${HOME}/meshtastic` (standalone binary)

## Configuration

### Setting Meshtastic CLI Path

If your Meshtastic CLI is not in PATH, edit each script:

**For Python scripts:**
```python
MESHTASTIC_CMD = "/path/to/meshtastic"
```

**For Bash scripts:**
```bash
MESHTASTIC="${HOME}/meshtastic"
```

### Specifying Serial Port

Most scripts support `--port` option:
```bash
./script-name.sh --port /dev/ttyACM0
```

Or set a default port by editing the script.

## Common Use Cases

### Daily Operations

```bash
# Morning: Check mesh health
./mesh-monitor.py

# Throughout day: Log all messages
./message-logger.py &

# Evening: Backup configurations
./backup-all-radios.sh
```

### Emergency Communications

```bash
# Send urgent broadcast
./emergency-broadcast.sh --urgent "Emergency message"

# Check who's online
./mesh-rollcall.sh
```

### Infrastructure Monitoring

```bash
# Monitor critical routers/repeaters
./node-health-alert.py --nodes !1152513c !42e9fe6f --interval 300
```

## Advanced Usage

### Running in Background (tmux/screen)

```bash
# Start logger in tmux
tmux new -s logger './message-logger.py'

# Start health monitor in background
nohup ./node-health-alert.py --nodes !6984a7c8 &
```

### Automation with Cron

```bash
# Backup daily at 2 AM
0 2 * * * /home/user/repos/meshtastic-scripts/backup-all-radios.sh

# Roll call every 6 hours
0 */6 * * * /home/user/repos/meshtastic-scripts/mesh-rollcall.sh > /tmp/rollcall.log
```

## Output Examples

### Mesh Monitor
```
════════════════════════════════════════════════════════════════════════════════
MESHTASTIC MESH MONITOR - 2026-01-11 11:30:45
════════════════════════════════════════════════════════════════════════════════

📊 MESH STATISTICS
  Total Nodes: 36
  Monitor Uptime: 0h 5m
  Nodes with SNR data: 28

📡 ACTIVE NODES
NODE ID      NAME                      SNR      HOPS   BATTERY  LAST HEARD
────────────────────────────────────────────────────────────────────────────────
!6984a7c8    CITADEL Mesh Client       ✓ 7.5dB  0      101%     1768130000
!b2a70de4    Meshtastic Rome           ✓ 6.2dB  0      N/A      1767911163
!42e9fe6f    W9BCI Brown Co Mesh-5     ~ 2.1dB  1      91%      1768000212
```

### Roll Call
```
═══════════════════════════════════════════════════════════
  MESH NETWORK ROLL CALL
═══════════════════════════════════════════════════════════

NODE ID         NAME                           STATUS
─────────────────────────────────────────────────────────────
!6984a7c8       CITADEL Mesh Client            ✓ Responded
!b2a70de4       Meshtastic Rome                ✓ Responded
!42e9fe6f       W9BCI Brown Co Mesh-5          ✗ No response

═══════════════════════════════════════════════════════════
  ROLL CALL SUMMARY
═══════════════════════════════════════════════════════════
Total Nodes:     36
Responded:       28
No Response:     8
Response Rate:   77.8%
```

## Troubleshooting

### Permission Denied
Ensure you're in the `dialout` group:
```bash
sudo usermod -a -G dialout $USER
newgrp dialout
```

### Device Not Found
Verify radio is attached to WSL2:
```bash
lsusb
ls -l /dev/ttyACM*
```

### Script Won't Execute
Make scripts executable:
```bash
chmod +x script-name.sh
```

## Contributing

Contributions welcome! Feel free to:
- Add new scripts
- Improve existing functionality
- Report bugs or suggest features
- Share your automation ideas

## Future Enhancements

Planned features:
- Web dashboard with real-time visualization
- Discord/Slack integration for alerts
- SQLite database for historical data
- MQTT bridge support
- GPS tracking and mapping
- Automated firmware updates
- Network topology visualization

## License

MIT License - feel free to use and modify as needed.

## Resources

- [Meshtastic Documentation](https://meshtastic.org/docs/)
- [Meshtastic Python CLI](https://github.com/meshtastic/python)
- [WSL2 Setup Guide](~/documentation/meshtastic/MESHTASTIC_WSL2_SETUP.md)
- [CLI Cheat Sheet](~/documentation/meshtastic/MESHTASTIC_CLI_CHEATSHEET.txt)

## Author

Created for the Meshtastic community. Happy meshing! 📡
