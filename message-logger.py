#!/usr/bin/env python3
"""
Meshtastic Message Logger
Logs all mesh messages to file with timestamps and metadata
"""

import subprocess
import sys
import os
from datetime import datetime
import argparse

MESHTASTIC_CMD = "meshtastic"

class MessageLogger:
    def __init__(self, port=None, logfile=None):
        self.port = port
        self.logfile = logfile or f"mesh-messages-{datetime.now().strftime('%Y%m%d')}.log"
        self.ensure_logfile()
        
    def ensure_logfile(self):
        """Create log file if it doesn't exist"""
        if not os.path.exists(self.logfile):
            with open(self.logfile, 'w') as f:
                f.write(f"# Meshtastic Message Log - Started {datetime.now()}\n")
                f.write("# Format: [TIMESTAMP] FROM -> TO | MESSAGE\n")
                f.write("-" * 80 + "\n")
    
    def log_message(self, timestamp, from_node, to_node, message, metadata=""):
        """Write message to log file"""
        log_entry = f"[{timestamp}] {from_node} -> {to_node} | {message}"
        if metadata:
            log_entry += f" ({metadata})"
        
        with open(self.logfile, 'a') as f:
            f.write(log_entry + "\n")
        
        # Also print to console
        print(log_entry)
    
    def listen(self):
        """Listen to mesh and log all messages"""
        cmd = [MESHTASTIC_CMD]
        if self.port:
            cmd.extend(["--port", self.port])
        cmd.append("--listen")
        
        print(f"📝 Listening for messages... (logging to {self.logfile})")
        print("Press Ctrl+C to stop\n")
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            for line in iter(process.stdout.readline, ''):
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Parse message format
                # Example: "From: !6984a7c8, To: ^all, Text: Hello mesh!"
                if "From:" in line and ("Text:" in line or "telemetry" in line.lower()):
                    # Extract from/to/message
                    parts = line.split(',')
                    from_node = "Unknown"
                    to_node = "Unknown"
                    message = line
                    
                    for part in parts:
                        if "From:" in part:
                            from_node = part.split("From:")[1].strip()
                        elif "To:" in part:
                            to_node = part.split("To:")[1].strip()
                        elif "Text:" in part:
                            message = part.split("Text:")[1].strip()
                    
                    self.log_message(timestamp, from_node, to_node, message)
                else:
                    # Log other events
                    with open(self.logfile, 'a') as f:
                        f.write(f"[{timestamp}] INFO: {line}\n")
                    print(f"[{timestamp}] INFO: {line}")
            
            process.wait()
            
        except KeyboardInterrupt:
            print("\n\n📝 Logging stopped. Messages saved to:", self.logfile)
            if process:
                process.terminate()
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Meshtastic Message Logger",
        epilog="""
Examples:
  %(prog)s
    Log messages to default file (mesh-messages-YYYYMMDD.log)
  
  %(prog)s --logfile custom.log
    Log to specific file
  
  %(prog)s --port /dev/ttyACM0
    Connect to specific radio
  
  %(prog)s --port /dev/ttyACM0 --logfile /var/log/mesh.log
    Specify both port and log file

Log format:
  [TIMESTAMP] FROM_NODE -> TO_NODE | MESSAGE_TEXT (metadata)

The logger captures:
  - Text messages between nodes
  - Telemetry data broadcasts
  - System events and notifications

Logs are written to both console and file. Press Ctrl+C to stop logging.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--port",
        metavar="DEVICE",
        help="serial port to connect to (e.g., /dev/ttyACM0). Auto-detects if not specified."
    )
    parser.add_argument(
        "--logfile",
        metavar="FILE",
        help="path to log file. Default: mesh-messages-YYYYMMDD.log in current directory."
    )
    args = parser.parse_args()
    
    logger = MessageLogger(port=args.port, logfile=args.logfile)
    logger.listen()

if __name__ == "__main__":
    main()
