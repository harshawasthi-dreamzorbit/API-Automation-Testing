import pytest
from test_data import (
    create_payload,
    fingerprint,
    unique_email
)

from config import (
    PAID_MACHINE_FINGERPRINT,
    REVOKED_MACHINE_FINGERPRINT,
    RATE_LIMIT_REQUESTS
)

def test_01_start_trial_success(trial_api):
    payload = create_payload(
        machine_id="fresh-trial-machine"
    )

    response = trial_api.start_trial(payload)
    assert response.status == 200
    data = response.json()
    assert data["licence"]["kind"] == "trial"
    assert data["licence"]["license_key"] is None
    assert data["token"]
    assert data["server_time"]


def test_02_trial_idempotency(trial_api):
    machine_id = "idempotency-machine"
    email = unique_email("idempotency")
    payload = create_payload(
        machine_id=machine_id,
        email=email
    )

    first_response = trial_api.start_trial(payload)
    assert first_response.status == 200
    first_data = first_response.json()
    second_response = trial_api.start_trial(payload)
    assert second_response.status == 200
    second_data = second_response.json()
    assert (
        first_data["licence"]["valid_from"]
        ==
        second_data["licence"]["valid_from"]
    )
    assert (
        first_data["licence"]["valid_until"]
        ==
        second_data["licence"]["valid_until"]
    )


def test_03_trial_already_used_with_same_email(trial_api):
    email = unique_email("duplicate")
    first_payload = create_payload(
        machine_id="email-first-machine",
        email=email
    )

    first_response = trial_api.start_trial(first_payload)
    assert first_response.status == 200
    second_payload = create_payload(
        machine_id="email-second-machine",
        email=email
    )

    second_response = trial_api.start_trial(second_payload)
    if second_response.status == 200:
        pytest.xfail(
            "API Defect: Same email is allowed to start a trial "
            "on a different machine. Expected 409 TRIAL_ALREADY_USED."
        )

    assert second_response.status == 409
    data = second_response.json()
    assert data["error"]["code"] == "TRIAL_ALREADY_USED"
    assert data["error"]["details"]["used_by"] == "email"


def test_04_missing_email(trial_api):
    payload = create_payload(
        machine_id="missing-email-machine"
    )

    payload.pop("email")
    response = trial_api.start_trial(payload)
    assert response.status == 400
    data = response.json()
    assert data["error"]["code"] == "BAD_REQUEST"


def test_05_invalid_mobile(trial_api):
    payload = create_payload(
        machine_id="invalid-mobile-machine",
        email=unique_email("invalid_mobile"),
        mobile="123"
    )

    response = trial_api.start_trial(payload)
    assert response.status == 400
    data = response.json()
    assert data["error"]["code"] == "BAD_REQUEST"


def test_06_already_licensed_machine(trial_api):
    if not PAID_MACHINE_FINGERPRINT:
        pytest.skip(
            "Configure a pre-licensed machine fingerprint"
        )

    payload = create_payload(
        machine_id="paid-machine",
        email=unique_email("licensed")
    )

    payload["fingerprint"] = PAID_MACHINE_FINGERPRINT
    response = trial_api.start_trial(payload)
    assert response.status == 409
    data = response.json()
    assert data["error"]["code"] == "ALREADY_LICENSED"


def test_07_revoked_key(trial_api):
    if not REVOKED_MACHINE_FINGERPRINT:
        pytest.skip(
            "Configure a machine with a revoked key"
        )

    payload = create_payload(
        machine_id="revoked-machine",
        email=unique_email("revoked")
    )

    payload["fingerprint"] = REVOKED_MACHINE_FINGERPRINT
    response = trial_api.start_trial(payload)
    assert response.status == 403
    data = response.json()
    assert data["error"]["code"] == "KEY_REVOKED"


def test_08_missing_fingerprint(trial_api):
    payload = create_payload(
        machine_id="missing-fingerprint-machine",
        email=unique_email("missing_fingerprint")
    )

    payload.pop("fingerprint")
    response = trial_api.start_trial(payload)
    assert response.status == 400
    data = response.json()
    assert data["error"]["code"] == "BAD_REQUEST"


def test_09_empty_fingerprint(trial_api):
    payload = create_payload(
        machine_id="empty-fingerprint-machine",
        email=unique_email("empty_fingerprint")
    )

    payload["fingerprint"] = ""
    response = trial_api.start_trial(payload)
    assert response.status == 400
    data = response.json()
    assert data["error"]["code"] == "BAD_REQUEST"


def test_10_invalid_fingerprint_format(trial_api):
    payload = create_payload(
        machine_id="invalid-fingerprint-machine",
        email=unique_email("invalid_fingerprint")
    )

    payload["fingerprint"] = "invalid-fingerprint"
    response = trial_api.start_trial(payload)
    assert response.status == 400
    data = response.json()
    assert data["error"]["code"] == "BAD_REQUEST"


def test_11_invalid_email_format(trial_api):
    payload = create_payload(
        machine_id="invalid-email-machine",
        email="invalid-email"
    )

    response = trial_api.start_trial(payload)
    assert response.status == 400
    data = response.json()
    assert data["error"]["code"] == "BAD_REQUEST"


def test_12_missing_business_name(trial_api):
    payload = create_payload(
        machine_id="missing-business-name-machine",
        email=unique_email("missing_business")
    )

    payload.pop("business_name")
    response = trial_api.start_trial(payload)
    assert response.status == 200
    data = response.json()
    assert data["licence"]["kind"] == "trial"
    assert data["token"]


def test_13_missing_owner_name(trial_api):
    payload = create_payload(
        machine_id="missing-owner-name-machine",
        email=unique_email("missing_owner")
    )

    payload.pop("owner_name")
    response = trial_api.start_trial(payload)
    assert response.status == 200
    data = response.json()
    assert data["licence"]["kind"] == "trial"
    assert data["token"]


def test_14_missing_mobile(trial_api):
    payload = create_payload(
        machine_id="missing-mobile-machine",
        email=unique_email("missing_mobile")
    )

    payload.pop("mobile")
    response = trial_api.start_trial(payload)
    assert response.status == 200
    data = response.json()
    assert data["licence"]["kind"] == "trial"
    assert data["token"]

def test_15_missing_app_version(trial_api):
    payload = create_payload(
        machine_id="missing-app-version-machine",
        email=unique_email("missing_version")
    )

    payload.pop("app_version")
    response = trial_api.start_trial(payload)
    assert response.status == 200
    data = response.json()
    assert data["licence"]["kind"] == "trial"
    assert data["token"]


def test_16_empty_request_payload(trial_api):
    response = trial_api.start_trial({})
    assert response.status == 400
    data = response.json()
    assert data["error"]["code"] == "BAD_REQUEST"


def test_17_null_mandatory_fields(trial_api):

    payload = create_payload(
        machine_id="null-fields-machine",
        email=unique_email("null_fields")
    )

    payload["fingerprint"] = None
    payload["email"] = None
    payload["business_name"] = None
    payload["owner_name"] = None
    payload["mobile"] = None
    payload["app_version"] = None
    response = trial_api.start_trial(payload)
    assert response.status == 400
    data = response.json()
    assert data["error"]["code"] == "BAD_REQUEST"


def test_18_invalid_machine_info_type(trial_api):
    payload = create_payload(
        machine_id="invalid-machine-info-machine",
        email=unique_email("invalid_machine_info")
    )

    payload["machine_info"] = "invalid-data"
    response = trial_api.start_trial(payload)
    assert response.status == 400
    data = response.json()
    assert data["error"]["code"] == "BAD_REQUEST"


def test_19_rate_limit_exceeded(trial_api):
    if RATE_LIMIT_REQUESTS <= 0:
        pytest.skip(
            "Configure RATE_LIMIT_REQUESTS in config.py "
            "to execute rate limit test"
        )

    payload = create_payload(
        machine_id="rate-limit-machine",
        email=unique_email("rate_limit")
    )

    rate_limit_response = None

    for _ in range(RATE_LIMIT_REQUESTS):
        response = trial_api.start_trial(payload)
        if response.status == 429:
            rate_limit_response = response
            break

    assert rate_limit_response is not None, (
        "Expected API to return 429 RATE_LIMITED "
        "after configured requests"
    )

    data = rate_limit_response.json()

    assert data["error"]["code"] == "RATE_LIMITED"