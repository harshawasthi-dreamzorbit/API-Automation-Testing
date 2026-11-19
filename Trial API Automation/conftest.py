import pytest
from playwright.sync_api import sync_playwright
from config import BASE_URL, HEADERS, TIMEOUT
from api_page import TrialAPIPage

@pytest.fixture(scope="module")
def api_context():
    with sync_playwright() as p:

        request = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers=HEADERS,
            timeout=TIMEOUT
        )
        yield request
        request.dispose()

@pytest.fixture(scope="module")
def trial_api(api_context):

    return TrialAPIPage(api_context)