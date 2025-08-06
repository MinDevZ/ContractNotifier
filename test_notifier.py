import unittest
from datetime import datetime
from notifier import process_contracts

class TestNotifier(unittest.TestCase):
    def setUp(self):
        self.contracts = [
            {
                "id": 1,
                "software_name": "A",
                "owner": "Alice",
                "organization": "Org",
                "annual_cost_eur": 12000,
                "renewal_date": "2025-08-01"
            }
        ]
        self.config = {
            "rules": [
                {"reason": "Urgent", "days_to_expiry": 3},
                {"reason": "High-Cost", "days_to_expiry": 30, "min_annual_cost": 10000},
                {"reason": "Upcoming", "days_to_expiry": 14}
            ],
            "priority": ["Urgent", "High-Cost", "Upcoming"]
        }

    def test_high_cost_notification(self):
        current_date = datetime.strptime("2025-07-02", "%Y-%m-%d")
        notifications, _ = process_contracts(self.contracts, self.config, {}, current_date)
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0]["reason"], "High-Cost")

    def test_urgent_priority(self):
        current_date = datetime.strptime("2025-07-30", "%Y-%m-%d")
        notification_log = {"1": {"notified_on": "2025-07-02", "reason": "High-Cost"}}
        notifications, _ = process_contracts(self.contracts, self.config, notification_log, current_date)
        self.assertEqual(notifications[0]["reason"], "Urgent")

    def test_no_repeat_lower_priority(self):
        current_date = datetime.strptime("2025-07-20", "%Y-%m-%d")
        notification_log = {"1": {"notified_on": "2025-07-15", "reason": "Upcoming"}}
        notifications, _ = process_contracts(self.contracts, self.config, notification_log, current_date)
        self.assertEqual(notifications[0]["reason"], "High-Cost")

    def test_no_repeat_same_priority(self):
        current_date = datetime.strptime("2025-07-21", "%Y-%m-%d")
        notification_log = {"1": {"notified_on": "2025-07-20", "reason": "High-Cost"}}
        notifications, _ = process_contracts(self.contracts, self.config, notification_log, current_date)
        self.assertEqual(len(notifications), 0)

if __name__ == '__main__':
    unittest.main()