import pytest
from playwright.sync_api import expect, sync_playwright


@pytest.mark.ui
@pytest.mark.smoke
def test_user_creates_booking(base_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(f"{base_url}/booking.html")
            page.get_by_label("Name").fill("Roman")
            page.get_by_label("Nights").fill("2")
            page.get_by_role("button", name="Create booking").click()
            expect(page.get_by_role("status")).to_have_text("Booking 101 created for Roman")
        finally:
            context.close()
            browser.close()


@pytest.mark.ui
@pytest.mark.regression
def test_ui_shows_api_validation_error(base_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(f"{base_url}/booking.html")
            page.get_by_label("Name").fill("Roman")
            page.get_by_label("Nights").evaluate("element => element.removeAttribute('min')")
            page.get_by_label("Nights").fill("0")
            page.get_by_role("button", name="Create booking").click()
            expect(page.get_by_role("status")).to_have_text("nights must be 1..28")
        finally:
            context.close()
            browser.close()
