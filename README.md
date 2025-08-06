# Contract Renewal Notifier

A tool for identifying and categorizing expiring contracts for renewal based on a set of prioritized notification rules.


## Setup

1. Clone the repository
2. Place your data in the `data/` directory:
   - `contracts.json`
   - `config.json`
   - `notification_log.json` (optional, auto-created)

## Running the Script

```bash
python main.py
```

To run the tests:
```bash
python -m unittest test_notifier.py
