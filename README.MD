#NUTManager
A simple WebUI for managing UPS devices via NUT

## Current Features
- List of UPS devices including statistics
    - UPS Name
    - Current Load (volt*current)
    - Current runtime (in seconds/minutes)
    - Battery charge percent
    - Current status (On-Line, Charging, Discharging)
- Global metrics for power usage and least runtime

## Installation
```bash
git clone https://github.com/owenrummage/UPS-Manager
cd UPS-Manager
pip install -r requirements.txt
cp .env.example .env

# Edit your .env file with the correct values

flask run
```