# Documentation

This directory contains comprehensive documentation for Meshtastic CLI setup and usage.

## Available Documents

### WSL2_SETUP.md

Complete technical guide for configuring Ubuntu on WSL2 to access Meshtastic radios via USB.

Contents:
- Windows configuration with usbipd-win
- WSL2 USB device permissions and udev rules
- Meshtastic CLI installation (pip and standalone)
- Verification procedures
- Troubleshooting guide
- Security considerations

**Audience:** Users setting up Meshtastic CLI on Windows with WSL2 for the first time.

### CLI_CHEATSHEET.txt

Quick reference guide for Meshtastic CLI commands in plaintext format for easy terminal access.

Contents:
- Basic connection commands
- Initial radio setup procedures
- Message sending and receiving
- Configuration management
- Channel operations
- Advanced features
- Troubleshooting tips
- Working with multiple radios

**Audience:** Operators who need quick command reference during daily operations.

**Usage:**
```bash
cat docs/CLI_CHEATSHEET.txt | less
grep -i "backup" docs/CLI_CHEATSHEET.txt
```

## Documentation Organization

```
docs/
├── README.md              # This file - documentation index
├── WSL2_SETUP.md         # Platform setup guide
└── CLI_CHEATSHEET.txt    # Command reference
```

## Additional Resources

For script-specific usage information, run any script with the `--help` flag:

```bash
./mesh-monitor.py --help
./message-logger.py --help
./emergency-broadcast.sh --help
```

## Contributing

Documentation improvements are welcome. When adding new documentation:

1. Place setup/configuration guides in Markdown format (`.md`)
2. Place quick reference materials in plaintext format (`.txt`)
3. Update this README.md with a description of the new document
4. Use clear, concise language appropriate for technical audiences
