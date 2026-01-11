#!/bin/bash
###############################################################################
# Backup All Connected Radios
# Creates timestamped configuration backups for all connected Meshtastic devices
###############################################################################

MESHTASTIC="${HOME}/meshtastic"
BACKUP_DIR="${HOME}/meshtastic-backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "═══════════════════════════════════════════════════════════"
echo "  MESHTASTIC RADIO BACKUP UTILITY"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Find all connected serial devices
DEVICES=$(ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null)

if [ -z "$DEVICES" ]; then
    echo -e "${RED}✗ No serial devices found${NC}"
    echo "Make sure your radio is connected and attached to WSL2"
    exit 1
fi

DEVICE_COUNT=$(echo "$DEVICES" | wc -l)
echo -e "Found ${GREEN}$DEVICE_COUNT${NC} serial device(s)"
echo ""

BACKUP_COUNT=0
FAILED_COUNT=0

# Backup each device
for device in $DEVICES; do
    echo "📡 Processing $device..."
    
    # Get node ID for filename
    NODE_ID=$($MESHTASTIC --port "$device" --info --timeout 15 2>/dev/null | grep -oP 'myNodeNum":\s*\K\d+' | head -1)
    
    if [ -z "$NODE_ID" ]; then
        echo -e "  ${RED}✗ Failed to connect${NC}"
        ((FAILED_COUNT++))
        continue
    fi
    
    # Get friendly name
    NODE_NAME=$($MESHTASTIC --port "$device" --info --timeout 10 2>/dev/null | grep -oP 'longName":\s*"\K[^"]+' | head -1)
    NODE_NAME=${NODE_NAME// /_}  # Replace spaces with underscores
    
    # Create backup filename
    BACKUP_FILE="${BACKUP_DIR}/backup-${NODE_NAME:-node${NODE_ID}}-${TIMESTAMP}.yaml"
    
    # Export configuration
    if $MESHTASTIC --port "$device" --export-config > "$BACKUP_FILE" 2>/dev/null; then
        SIZE=$(stat -f %z "$BACKUP_FILE" 2>/dev/null || stat -c %s "$BACKUP_FILE" 2>/dev/null)
        echo -e "  ${GREEN}✓ Backup saved${NC} → $BACKUP_FILE (${SIZE} bytes)"
        ((BACKUP_COUNT++))
    else
        echo -e "  ${RED}✗ Backup failed${NC}"
        rm -f "$BACKUP_FILE"
        ((FAILED_COUNT++))
    fi
    
    echo ""
done

# Summary
echo "═══════════════════════════════════════════════════════════"
echo "  BACKUP SUMMARY"
echo "═══════════════════════════════════════════════════════════"
echo -e "Devices Found:      ${YELLOW}$DEVICE_COUNT${NC}"
echo -e "Successful Backups: ${GREEN}$BACKUP_COUNT${NC}"
echo -e "Failed Backups:     ${RED}$FAILED_COUNT${NC}"
echo -e "Backup Location:    ${BACKUP_DIR}"
echo ""

# List recent backups
echo "Recent backups:"
ls -lht "$BACKUP_DIR" | head -6 | tail -5

exit 0
