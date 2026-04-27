#!/usr/bin/env bash
# Set up the pidog systemd service so ROS 2 starts on boot.
# Runs on the Pi — called by setup-pi.sh or directly: bash ~/setup-service.sh

set -euo pipefail

echo "--- Setting up pidog systemd service ---"

chmod +x "$HOME/start-pidog.sh"

sudo cp "$HOME/pidog.service" /etc/systemd/system/pidog.service

sudo systemctl daemon-reload
sudo systemctl enable pidog
echo "  pidog service enabled — starts on boot"
echo "  Manage with: sudo systemctl start|stop|status pidog"
echo "  View logs:   journalctl -u pidog -f"
