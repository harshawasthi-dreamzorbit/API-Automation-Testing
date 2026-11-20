# Trial API Automation Framework

## Overview
API automation framework for testing the Trial Start API using Python, Playwright, and Pytest.

## Framework Design
The project follows the Page Object Model (POM) design pattern to separate API operations, test data, configuration, and test cases.

## Tech Stack
- Python
- Playwright
- Pytest

## Project Structure
- `config.py` – Configuration and endpoint settings
- `test_data.py` – Payload and test data generation
- `api_page.py` – API request handling
- `conftest.py` – Pytest fixtures
- `test_trial_api.py` – API test scenarios

## Execution

```bash
pytest test_trial_api.py -v -s
```

## Reporting

```bash
pytest test_trial_api.py -v -s --html=trial_api_report.html --self-contained-html
```

## Test Coverage
Includes positive, negative, validation, idempotency, and edge-case scenarios.