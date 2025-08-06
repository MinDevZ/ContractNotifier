from datetime import datetime

def determine_reason(contract, config, current_date):
    days_to_expiry = (datetime.strptime(contract["renewal_date"], "%Y-%m-%d") - current_date).days
    for reason in config["priority"]:
        for rule in config["rules"]:
            if rule["reason"] == reason:
                if days_to_expiry <= rule["days_to_expiry"]:
                    if reason == "High-Cost" and contract["annual_cost_eur"] < rule.get("min_annual_cost", 0):
                        continue
                    return reason

    return None

def process_contracts(contracts, config, notification_log, current_date):
    new_notifications = []
    updated_log = notification_log.copy()

    for contract in contracts:
        contract_id = str(contract["id"])
        reason = determine_reason(contract, config, current_date)
        if not reason:
            continue

        previous = notification_log.get(contract_id)
        if previous:
            if config["priority"].index(reason) < config["priority"].index(previous["reason"]):
                pass
            else:
                continue

        contract_with_reason = contract.copy()
        contract_with_reason["reason"] = reason
        new_notifications.append(contract_with_reason)

        updated_log[contract_id] = {
            "notified_on": current_date.strftime("%Y-%m-%d"),
            "reason": reason
        }

    return new_notifications, updated_log