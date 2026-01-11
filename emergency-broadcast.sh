#!/bin/bash
###############################################################################
# Emergency Broadcast System
# Send urgent messages to all nodes with confirmation
###############################################################################

MESHTASTIC="${HOME}/meshtastic"
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Usage
usage() {
    cat << 'EOF'
Meshtastic Emergency Broadcast System

USAGE:
  emergency-broadcast.sh [OPTIONS] "MESSAGE"

OPTIONS:
  --port DEVICE     Serial port (e.g., /dev/ttyACM0)
                    Auto-detects if not specified
  
  --ack             Wait for message acknowledgment from nodes
  
  --urgent          Prepend [URGENT] prefix to message
  
  -h, --help        Display this help message

DESCRIPTION:
  Broadcasts a message to all nodes in the mesh network (destination: ^all).
  Includes interactive confirmation prompt before transmission to prevent
  accidental broadcasts.

EXAMPLES:
  emergency-broadcast.sh "Meeting at 1500h"
    Simple broadcast to all nodes
  
  emergency-broadcast.sh --urgent "Emergency evacuation"
    Urgent broadcast with priority prefix
  
  emergency-broadcast.sh --ack --port /dev/ttyACM0 "Check in required"
    Broadcast with acknowledgment on specific radio

NOTES:
  - Always confirms before sending to prevent mistakes
  - Messages broadcast to ^all destination (all mesh nodes)
  - Urgent flag adds [URGENT] prefix for operator attention
  - Acknowledgment flag waits for node responses (slower)

EOF
    exit 1
}

# Parse arguments
PORT=""
ACK=""
URGENT=""
MESSAGE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --port)
            PORT="--port $2"
            shift 2
            ;;
        --ack)
            ACK="--ack"
            shift
            ;;
        --urgent)
            URGENT="[URGENT] "
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            MESSAGE="$1"
            shift
            ;;
    esac
done

# Validate message
if [ -z "$MESSAGE" ]; then
    echo -e "${RED}Error: No message provided${NC}"
    usage
fi

# Add urgent prefix if requested
FULL_MESSAGE="${URGENT}${MESSAGE}"

# Confirm before sending
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  EMERGENCY BROADCAST SYSTEM${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Message: ${GREEN}${FULL_MESSAGE}${NC}"
echo -e "Destination: ${GREEN}All nodes (^all)${NC}"
[ -n "$ACK" ] && echo -e "Acknowledgment: ${GREEN}Enabled${NC}"
echo ""
echo -e "${YELLOW}This will broadcast to ALL nodes in the mesh.${NC}"
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Broadcast cancelled."
    exit 0
fi

# Send message
echo ""
echo "📡 Broadcasting message..."
if $MESHTASTIC $PORT --sendtext "$FULL_MESSAGE" --dest ^all $ACK; then
    echo -e "${GREEN}✓ Message sent successfully${NC}"
else
    echo -e "${RED}✗ Failed to send message${NC}"
    exit 1
fi
