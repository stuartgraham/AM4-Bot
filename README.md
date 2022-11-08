# AM4-Bot
Bot for Airline Manager 4 operations that runs in Docker.

## Features
- Purchase maximum fuel and CO2 when under threshold
- Random checks every 30 minutes to verify price changes
- Dispatches all aircraft

## Useful commands
Container users `USERNAME` and `PASSWORD` environment variables to access the sim UI.

**Docker**

`docker run ghcr.io/stuartgraham/am4-bot:latest`

**Docker Compose**

```
version: "3.9"
services:
  am4bot:
    image: ghcr.io/stuartgraham/am4-bot:latest
    restart: unless-stopped
    container_name: am4-bot
    environment:
      - USERNAME=some@user.com
      - PASSWORD=somepassword!
```
