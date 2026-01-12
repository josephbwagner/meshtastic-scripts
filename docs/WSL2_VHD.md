# WSL 2 Ubuntu VHD Setup Guide

## Overview
Automatically mount a VHD in WSL 2 Ubuntu on Windows startup.

## Prerequisites
- Windows 10/11 with WSL 2
- Ubuntu WSL 2 distribution
- Administrator privileges

## Setup Process

### 1. Create VHD
Use Windows Disk Management or `diskpart` to create a VHD file (e.g., `E:\ubuntudisk.vhd`).

### 2. Initial Mount & Format
Mount and format the VHD in WSL:

```powershell
# Windows (Admin PowerShell)
wsl --mount E:\ubuntudisk.vhd --vhd --bare
```

```bash
# Ubuntu
sudo mkfs.ext4 /dev/sdd
sudo mkdir -p /mnt/vhd
sudo mount /dev/sdd /mnt/vhd
```

### 3. Configure UUID Mounting
Get the UUID and add to fstab:

```bash
sudo blkid /dev/sdd
# Note the UUID (e.g., be152bd1-1c0c-4657-96b1-dea4f6e4f4bb)
```

Add to `/etc/fstab`:
```
UUID="be152bd1-1c0c-4657-96b1-dea4f6e4f4bb" /mnt/vhd ext4 defaults,nofail 0 0
```

### 4. Automate Windows Mount
Create a Task Scheduler task:
- **Trigger**: At startup
- **Action**: `wsl.exe --mount E:\ubuntudisk.vhd --vhd --bare`
- **Run with highest privileges**: Enabled

## Usage

### Manual Mount
```powershell
# Windows (Admin)
wsl --mount E:\ubuntudisk.vhd --vhd --bare
```

### Access Files
```bash
# Ubuntu
ls /mnt/vhd
```

## Notes
- Device names may vary (`/dev/sdd`, `/dev/sda`, etc.)
- UUID mounting ensures consistent access
- Startup error `wsl: Processing /etc/fstab with mount -a failed.` can be ignored with fstab option `nofail`
- VHD mounts automatically on system startup
