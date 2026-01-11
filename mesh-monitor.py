#!/usr/bin/env python3
"""
Meshtastic Mesh Monitor
Real-time monitoring of mesh network health and activity
"""

import subprocess
import json
import time
import sys
from datetime import datetime
from collections import defaultdict

MESHTASTIC_CMD = "meshtastic"

class MeshMonitor:
    def __init__(self, port=None):
        self.port = port
        self.node_history = defaultdict(list)
        self.message_count = 0
        self.start_time = time.time()
        
    def get_mesh_cmd(self):
        if self.port:
            return [MESHTASTIC_CMD, "--port", self.port]
        return [MESHTASTIC_CMD]
    
    def get_node_info(self):
        """Fetch current node information"""
        try:
            cmd = self.get_mesh_cmd() + ["--nodes", "--no-time"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout
        except subprocess.TimeoutExpired:
            return None
        except Exception as e:
            print(f"Error fetching nodes: {e}", file=sys.stderr)
            return None
    
    def parse_nodes(self, output):
        """Parse node output into structured data"""
        nodes = {}
        current_node = None
        
        for line in output.split('\n'):
            if line.startswith('  '):
                # Node data line
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    if current_node and key and value:
                        nodes[current_node][key.strip()] = value.strip()
            else:
                # New node header
                node_id = line.strip()
                if node_id.startswith('!'):
                    current_node = node_id
                    nodes[current_node] = {}
        
        return nodes
    
    def display_dashboard(self):
        """Display real-time dashboard"""
        while True:
            try:
                # Clear screen
                print("\033[2J\033[H", end='')
                
                # Header
                print("=" * 80)
                print(f"MESHTASTIC MESH MONITOR - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("=" * 80)
                
                # Get node info
                output = self.get_node_info()
                if not output:
                    print("⚠ Unable to fetch node information")
                    time.sleep(5)
                    continue
                
                nodes = self.parse_nodes(output)
                
                # Statistics
                uptime = time.time() - self.start_time
                print(f"\n📊 MESH STATISTICS")
                print(f"  Total Nodes: {len(nodes)}")
                print(f"  Monitor Uptime: {int(uptime // 3600)}h {int((uptime % 3600) // 60)}m")
                
                # Count nodes by SNR
                online_nodes = sum(1 for n in nodes.values() if 'SNR' in n)
                print(f"  Nodes with SNR data: {online_nodes}")
                
                # Node list with key info
                print(f"\n📡 ACTIVE NODES")
                print(f"{'NODE ID':<12} {'NAME':<25} {'SNR':<8} {'HOPS':<6} {'BATTERY':<8} {'LAST HEARD'}")
                print("-" * 80)
                
                for node_id, data in sorted(nodes.items()):
                    name = data.get('User', 'Unknown')[:25]
                    snr = data.get('SNR', 'N/A')
                    hops = data.get('Hops Away', 'N/A')
                    battery = data.get('Battery', 'N/A')
                    last_heard = data.get('LastHeard', 'N/A')
                    
                    # Color code by SNR
                    if snr != 'N/A':
                        try:
                            snr_val = float(snr.replace('dB', '').strip())
                            if snr_val > 5:
                                snr = f"✓ {snr}"
                            elif snr_val > 0:
                                snr = f"~ {snr}"
                            else:
                                snr = f"✗ {snr}"
                        except:
                            pass
                    
                    print(f"{node_id:<12} {name:<25} {snr:<8} {hops:<6} {battery:<8} {last_heard}")
                
                print("\n" + "=" * 80)
                print("Press Ctrl+C to exit")
                
                # Update every 30 seconds
                time.sleep(30)
                
            except KeyboardInterrupt:
                print("\n\nMonitoring stopped.")
                sys.exit(0)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                time.sleep(5)

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Meshtastic Mesh Network Monitor",
        epilog="""
Examples:
  %(prog)s
    Auto-detect radio and display live dashboard
  
  %(prog)s --port /dev/ttyACM0
    Monitor specific radio on /dev/ttyACM0
  
  %(prog)s --port /dev/serial/by-id/usb-Heltec_...
    Use persistent device identifier

Dashboard displays:
  - Total node count and network statistics
  - Node-by-node details including SNR, battery, and hop count
  - Signal quality indicators (good/moderate/poor)
  - Real-time updates every 30 seconds

Press Ctrl+C to exit the monitor.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--port",
        metavar="DEVICE",
        help="serial port to connect to (e.g., /dev/ttyACM0). If not specified, will auto-detect."
    )
    args = parser.parse_args()
    
    monitor = MeshMonitor(port=args.port)
    monitor.display_dashboard()

if __name__ == "__main__":
    main()
