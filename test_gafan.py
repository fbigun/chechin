import os
import pytest
from playwright import sync_playwright

@pytest.fixture(scope="session")
def page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.newContext()
        page = context.newPage()
        yield page
        page.close()
        context.close()
        browser.close()

@pytest.fixture
def gafan(page):
    page.goto("https://xn--sft464f.ga/auth/login")
    page.click("input[name=\"Email\"]")
    page.fill("input[name=\"Email\"]", os.getenv("USERNAME"))
    page.click("input[name=\"Password\"]")
    page.fill("input[name=\"Password\"]", os.getenv("PASSWD"))
    page.click("text=/.*确认登录.*/")
    page.waitForSelector("text=/.*知道了.*/")
    page.click("text=/.*知道了.*/")
    return page

def test_checkin(gafan):
    page = gafan
    page.goto("https://xn--sft464f.ga/user")
    assert page.url == "https://xn--sft464f.ga/user"
    page.waitForSelector("text=/.*点我签到.*/")
    page.click("text=/.*点我签到.*/")
    page.waitForSelector("text=/.*已签到.*/")
