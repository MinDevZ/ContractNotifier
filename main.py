import json
from datetime import datetime
from notifier import process_contracts
from utils import load_json, save_json

CURRENT_DATE = datetime.strptime("2025-07-30", "%Y-%m-%d")

config = load_json("data/config.json", [])
contracts = load_json("data/contracts.json")
notification_log = load_json("data/notification_log.json", {})

notifications, updated_log = process_contracts(contracts, config, notification_log, CURRENT_DATE)

print(json.dumps(notifications, indent=2))

save_json("data/notification_log.json", updated_log)