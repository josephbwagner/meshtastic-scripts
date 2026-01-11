#!/bin/bash
###############################################################################
# Mesh Roll Call
# Request telemetry from all known nodes and report who responds
###############################################################################

MESHTASTIC="${HOME}/meshtastic"
TIMEOUT=60
TMPFILE="/tmp/mesh-rollcall-$$.txt"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Usage
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    cat << 'EOF'
Meshtastic Network Roll Call

USAGE:
  mesh-rollcall.sh [OPTIONS]

OPTIONS:
  --port DEVICE     Serial port (e.g., /dev/ttyACM0)
                    Auto-detects if not specified
  
  -h, --help        Display this help message

DESCRIPTION:
  Performs a network health check by requesting telemetry from all known
  nodes in the mesh database. Reports which nodes respond and calculates
  overall network response rate.

PROCESS:
  1. Fetches complete node list from local database
  2. Requests telemetry from each node sequentially
  3. Records response/no-response status for each node
  4. Generates summary report with statistics

OUTPUT:
  - Per-node status (responded or no response)
  - Node names and identifiers
  - Total count and response rate percentage

EXAMPLES:
  mesh-rollcall.sh
    Run roll call on auto-detected radio
  
  mesh-rollcall.sh --port /dev/ttyACM0
    Run on specific radio device

NOTES:
  - Takes time to complete (2 seconds per node)
  - Non-responsive nodes may be offline, out of range, or powered down
  - Network conditions can affect response rates
  - Recommended to run during quiet periods for accurate results

EOF
    exit 0
fi

echo "═══════════════════════════════════════════════════════════"
echo "  MESH NETWORK ROLL CALL"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Parse port option
PORT=""
if [ "$1" == "--port" ]; then
    PORT="--port $2"
    shift 2
fi

# Get list of nodes
echo "📡 Fetching node list..."
$MESHTASTIC $PORT --nodes --no-time > "$TMPFILE"

if [ ! -s "$TMPFILE" ]; then
    echo -e "${RED}✗ Failed to fetch nodes${NC}"
    rm -f "$TMPFILE"
    exit 1
fi

# Extract node IDs
NODE_IDS=$(grep -oP '!\w+' "$TMPFILE" | sort -u)
NODE_COUNT=$(echo "$NODE_IDS" | wc -l)

echo -e "Found ${GREEN}$NODE_COUNT${NC} nodes in database"
echo ""
echo "Requesting telemetry from all nodes (this may take a while)..."
echo ""

# Request telemetry from each node
RESPONDED=0
NO_RESPONSE=0

printf "%-15s %-30s %s\n" "NODE ID" "NAME" "STATUS"
echo "─────────────────────────────────────────────────────────────"

for node_id in $NODE_IDS; do
    # Get node name
    NODE_NAME=$(grep -A 5 "$node_id" "$TMPFILE" | grep "User:" | head -1 | cut -d: -f2- | xargs)
    
    # Request telemetry
    if timeout 10 $MESHTASTIC $PORT --request-telemetry --dest "$node_id" --timeout 10 &>/dev/null; then
        printf "%-15s %-30s ${GREEN}✓ Responded${NC}\n" "$node_id" "$NODE_NAME"
        ((RESPONDED++))
    else
        printf "%-15s %-30s ${RED}✗ No response${NC}\n" "$node_id" "$NODE_NAME"
        ((NO_RESPONSE++))
    fi
    
    # Small delay between requests
    sleep 2
done

# Summary
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  ROLL CALL SUMMARY"
echo "═══════════════════════════════════════════════════════════"
echo -e "Total Nodes:     ${YELLOW}$NODE_COUNT${NC}"
echo -e "Responded:       ${GREEN}$RESPONDED${NC}"
echo -e "No Response:     ${RED}$NO_RESPONSE${NC}"
echo -e "Response Rate:   $(awk "BEGIN {printf \"%.1f%%\", ($RESPONDED/$NODE_COUNT)*100}")"
echo ""

# Cleanup
rm -f "$TMPFILE"
