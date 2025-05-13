# Infrastructure

This folder contains infrastructure-related configuration for deploying the Feedback project.

## Files

- `feedback.service`: systemd unit file for running the full project via Docker Compose on server boot.

## Usage

1. Copy `feedback.service` to `/etc/systemd/system/`:
   ```bash
   sudo cp utils/feedback.service /etc/systemd/system/
   ```

2. Reload systemd:
   ```bash
   sudo systemctl daemon-reload
   ```

3. Enable the service on boot:
   ```bash
   sudo systemctl enable feedback
   ```

4. Start the service:
   ```bash
   sudo systemctl start feedback
   ```

To stop:
```bash
sudo systemctl stop feedback
```
