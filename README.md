# Meshtastic Scripts

Automation and monitoring tools for Meshtastic mesh radio networks.

## Overview

This collection provides command-line utilities for managing Meshtastic networks using the Python CLI. Scripts are designed for production use with comprehensive error handling and detailed help documentation.

## Available Scripts

### mesh-monitor.py

Real-time monitoring dashboard displaying mesh network health and node status.

Features:
- Live node statistics including SNR, battery levels, and hop counts
- Automatic refresh with configurable intervals
- Signal quality indicators for quick health assessment
- Support for monitoring specific devices via serial port selection

Run with `--help` for detailed usage information.

### message-logger.py

Message archival system that captures all mesh network traffic.

Features:
- Timestamped logging of all messages and events
- Structured output format for parsing and analysis
- Automatic daily log file rotation
- Captures both text messages and telemetry data

Run with `--help` for detailed usage information.

### emergency-broadcast.sh

Broadcast urgent messages to all mesh nodes with safety confirmations.

Features:
- Interactive confirmation before transmission
- Optional urgent message prefix for priority alerts
- Acknowledgment request support
- Serial port specification for multi-radio setups

Run with `--help` for detailed usage information.

### mesh-rollcall.sh

Network health check tool that polls all known nodes for responsiveness.

Features:
- Systematic telemetry requests to all registered nodes
- Response rate calculation and reporting
- Identification of offline or unresponsive nodes
- Detailed status output with node names and identifiers

Run with `--help` for detailed usage information.

### backup-all-radios.sh

Automated configuration backup utility for all connected radios.

Features:
- Automatic detection of connected Meshtastic devices
- Timestamped backup files with descriptive naming
- Individual success/failure reporting per device
- Centralized backup storage in dedicated directory

Run with `--help` for detailed usage information.

### node-health-alert.py

Continuous monitoring system for critical infrastructure nodes.

Features:
- Configurable monitoring of specified critical nodes
- Battery level alerts with adjustable thresholds
- Signal quality degradation warnings
- Offline node detection with alert generation
- Rate-limited notifications to prevent alert fatigue

Run with `--help` for detailed usage information.

## Requirements

- Meshtastic CLI (standalone binary or installed via pip)
- Python 3.6 or later
- Bash shell environment
- Linux, WSL2, or macOS

## Installation

Clone the repository and make scripts executable:

```bash
git clone https://github.com/yourusername/meshtastic-scripts.git
cd meshtastic-scripts
chmod +x *.sh *.py
```

## Configuration

Scripts default to using `meshtastic` command from PATH. If using a standalone binary or custom installation path, edit the `MESHTASTIC_CMD` variable at the top of each script.

All scripts support the `--help` flag for detailed usage information and available options.

## Usage

Run any script with the `--help` flag to see detailed documentation:

```bash
./mesh-monitor.py --help
./message-logger.py --help
./emergency-broadcast.sh --help
./mesh-rollcall.sh --help
./backup-all-radios.sh --help
./node-health-alert.py --help
```

Most scripts support the `--port` option to specify a serial device when multiple radios are connected.

## Common Workflows

Monitor network health:
```bash
./mesh-monitor.py
```

Log all network traffic:
```bash
./message-logger.py
```

Backup all connected devices:
```bash
./backup-all-radios.sh
```

Check network responsiveness:
```bash
./mesh-rollcall.sh
```

Monitor critical infrastructure:
```bash
./node-health-alert.py --nodes !6984a7c8 !b2a70de4
```

## Background Execution

For continuous monitoring, run scripts in tmux, screen, or as background processes:

```bash
tmux new -s monitor './mesh-monitor.py'
nohup ./message-logger.py > /dev/null 2>&1 &
```

## Automation

Scripts can be scheduled via cron for periodic execution:

```bash
# Backup configurations daily at 2 AM
0 2 * * * /path/to/backup-all-radios.sh

# Network health check every 6 hours
0 */6 * * * /path/to/mesh-rollcall.sh
```

## License

MIT License

## Resources

- Meshtastic Documentation: https://meshtastic.org/docs/
- Meshtastic Python CLI: https://github.com/meshtastic/python
