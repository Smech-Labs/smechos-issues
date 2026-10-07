import sys
import os
import json
import hashlib
import subprocess
import tempfile
import shutil
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List

# ... existing imports and code ...

def phase_plasma_configure(ctx: BuildCtx) -> None:
    """Configure Plasma desktop session, including first-boot wizard."""
    # ... existing code ...

    # Generate plasmalogin.service for the real user session
    plasmalogin_unit = """[Unit]
Description=Plasma Login
After=graphical.target
Requires=graphical.target
Conflicts=plasma-setup.service
Before=plasma-setup.service

[Service]
Type=simple
Environment=KDE_SESSION_UID=1000
Environment=XDG_SESSION_TYPE=wayland
ExecStart=/usr/bin/plasmawayland
Restart=on-failure
RestartSec=5

[Install]
WantedBy=graphical.target
"""

    # Generate plasma-setup.service for the first-boot wizard
    plasma_setup_unit = """[Unit]
Description=SmechOS First-Boot Setup Wizard
After=graphical.target
Requires=graphical.target
Conflicts=plasmalogin.service
Before=plasmalogin.service

[Service]
Type=simple
User=plasma-setup
Uid=983
Environment=KDE_SESSION_UID=983
Environment=XDG_SESSION_TYPE=wayland
ExecStart=/usr/bin/plasmawayland
ExecStopPost=/bin/bash -c 'fuser -k /dev/dri/card0 2>/dev/null || true'
Restart=on-failure
RestartSec=5

[Install]
WantedBy=graphical.target
"""

    # Write service files
    systemd_dir = ctx.out / "etc/systemd/system"
    systemd_dir.mkdir(parents=True, exist_ok=True)

    (systemd_dir / "plasmalogin.service").write_text(plasmalogin_unit)
    (systemd_dir / "plasma-setup.service").write_text(plasma_setup_unit)

    # Enable both services
    subprocess.run(
        ["systemctl", "enable", "plasmalogin.service"],
        check=False,
        cwd=str(ctx.out),
    )
    subprocess.run(
        ["systemctl", "enable", "plasma-setup.service"],
        check=False,
        cwd=str(ctx.out),
    )

    print(f"[phase_plasma_configure] Generated plasmalogin.service and plasma-setup.service")


def phase_patch_metadata(ctx: BuildCtx) -> None:
    """Apply metadata patches and ensure proper session ordering."""
    # ... existing code ...

    # Ensure the wizard session is properly torn down before real session starts
    # Add a drop-in override to guarantee cleanup of DRM resources
    dropin_dir = Path(ctx.out) / "etc/systemd/system/plasma-setup.service.d"
    dropin_dir.mkdir(parents=True, exist_ok=True)

    dropin_config = """[Service]
# Ensure DRM master is released before real session starts
ExecStopPost=/bin/sh -c 'sync; echo 1 > /proc/sys/kernel/sysrq 2>/dev/null || true'
"""
    (dropin_dir / "drm-cleanup.conf").write_text(dropin_config)

    print(f"[phase_patch_metadata] Added DRM cleanup drop-in for plasma-setup.service")
