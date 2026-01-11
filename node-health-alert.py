#!/usr/bin/env python3
"""
Node Health Alerter
Monitor specific critical nodes and alert when they go offline or battery is low
"""

import subprocess
import time
import sys
from datetime import datetime
import argparse

MESHTASTIC_CMD = "meshtastic"
CHECK_INTERVAL = 300  # 5 minutes
BATTERY_THRESHOLD = 20  # Alert if battery below 20%

class NodeHealthMonitor:
    def __init__(self, port=None, critical_nodes=None):
        self.port = port
        self.critical_nodes = critical_nodes or []
        self.last_seen = {}
        self.battery_status = {}
        self.alert_count = {}
        
    def get_mesh_cmd(self):
        if self.port:
            return [MESHTASTIC_CMD, "--port", self.port]
        return [MESHTASTIC_CMD]
    
    def get_nodes(self):
        """Fetch current node list"""
        try:
            cmd = self.get_mesh_cmd() + ["--nodes", "--no-time"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout
        except Exception as e:
            print(f"Error fetching nodes: {e}", file=sys.stderr)
            return None
    
    def parse_node_data(self, output, node_id):
        """Extract data for specific node"""
        lines = output.split('\n')
        in_target_node = False
        node_data = {}
        
        for line in lines:
            if line.strip() == node_id:
                in_target_node = True
                continue
            
            if in_target_node:
                if line.startswith('!'):  # Next node
                    break
                if ':' in line:
                    key, value = line.split(':', 1)
                    node_data[key.strip()] = value.strip()
        
        return node_data
    
    def check_node_health(self, node_id, node_data):
        """Check if node is healthy and return alert messages"""
        alerts = []
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Check if node is present
        if not node_data:
            if node_id in self.last_seen:
                alerts.append(f"[{timestamp}] ⚠️ ALERT: Node {node_id} is OFFLINE (not in node list)")
            return alerts
        
        # Update last seen
        self.last_seen[node_id] = time.time()
        
        # Check battery level
        battery_str = node_data.get('Battery', '')
        if battery_str and '%' in battery_str:
            try:
                battery_level = int(battery_str.replace('%', '').strip())
                
                if battery_level <= BATTERY_THRESHOLD:
                    alert_key = f"{node_id}_battery"
                    if alert_key not in self.alert_count or \
                       (time.time() - self.alert_count[alert_key]) > 3600:  # Alert max once per hour
                        alerts.append(f"[{timestamp}] 🔋 ALERT: Node {node_id} battery LOW: {battery_level}%")
                        self.alert_count[alert_key] = time.time()
                
                self.battery_status[node_id] = battery_level
            except ValueError:
                pass
        
        # Check SNR (signal quality)
        snr_str = node_data.get('SNR', '')
        if snr_str and 'dB' in snr_str:
            try:
                snr = float(snr_str.replace('dB', '').strip())
                if snr < -10:
                    alert_key = f"{node_id}_snr"
                    if alert_key not in self.alert_count or \
                       (time.time() - self.alert_count[alert_key]) > 3600:
                        alerts.append(f"[{timestamp}] 📡 WARNING: Node {node_id} has WEAK signal: {snr}dB")
                        self.alert_count[alert_key] = time.time()
            except ValueError:
                pass
        
        return alerts
    
    def monitor(self):
        """Main monitoring loop"""
        print("=" * 80)
        print("NODE HEALTH MONITOR")
        print("=" * 80)
        print(f"Monitoring {len(self.critical_nodes)} critical node(s)")
        print(f"Check interval: {CHECK_INTERVAL} seconds")
        print(f"Battery alert threshold: {BATTERY_THRESHOLD}%")
        print("Press Ctrl+C to stop\n")
        
        cycle = 0
        
        try:
            while True:
                cycle += 1
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{timestamp}] Check cycle #{cycle}")
                
                # Fetch node list
                output = self.get_nodes()
                if not output:
                    print("  ⚠️ Failed to fetch node list")
                    time.sleep(CHECK_INTERVAL)
                    continue
                
                # Check each critical node
                for node_id in self.critical_nodes:
                    node_data = self.parse_node_data(output, node_id)
                    alerts = self.check_node_health(node_id, node_data)
                    
                    if alerts:
                        for alert in alerts:
                            print(alert)
                            # Here you could add email, SMS, or Discord notifications
                    else:
                        battery = self.battery_status.get(node_id, 'N/A')
                        print(f"  ✓ {node_id} is healthy (Battery: {battery}%)")
                
                print()
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped.")
            sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Monitor critical Meshtastic nodes")
    parser.add_argument("--port", help="Serial port (e.g., /dev/ttyACM0)")
    parser.add_argument("--nodes", nargs='+', required=True,
                       help="Node IDs to monitor (e.g., !6984a7c8 !b2a70de4)")
    parser.add_argument("--interval", type=int, default=300,
                       help="Check interval in seconds (default: 300)")
    parser.add_argument("--battery-threshold", type=int, default=20,
                       help="Battery alert threshold percentage (default: 20)")
    
    args = parser.parse_args()
    
    global CHECK_INTERVAL, BATTERY_THRESHOLD
    CHECK_INTERVAL = args.interval
    BATTERY_THRESHOLD = args.battery_threshold
    
    monitor = NodeHealthMonitor(port=args.port, critical_nodes=args.nodes)
    monitor.monitor()

if __name__ == "__main__":
    main()
