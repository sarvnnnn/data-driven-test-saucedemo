import pytest
import pandas as pd
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# =============================================
#   Data-Driven Test Pipeline — SauceDemo
#   Reads users from CSV and tests each one
# =============================================

# 🔧 CONFIG
SLACK_WEBHOOK = "YOUR_SLACK_WEBHOOK_URL"
BASE_URL      = "https://www.saucedemo.com"
CSV_FILE      = "users.csv"

# -----------------------------------------------
# LOAD USERS FROM CSV
# -----------------------------------------------
def load_users():
    df = pd.read_csv(CSV_FILE)
    return [(row["username"], row["password"], row["expected"]) for _, row in df.iterrows()]

# -----------------------------------------------
# SETUP — browser fixture
# -----------------------------------------------
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield driver
    driver.quit()

# -----------------------------------------------
# HELPER — send to Slack
# -----------------------------------------------
def send_to_slack(message):
    if SLACK_WEBHOOK == "YOUR_SLACK_WEBHOOK_URL":
        print("⚠️  Slack webhook not set — skipping")
        return
    requests.post(SLACK_WEBHOOK, json={"text": message})

# -----------------------------------------------
# DATA DRIVEN TEST — Login with each user
# -----------------------------------------------
results = []

@pytest.mark.parametrize("username,password,expected", load_users())
def test_login_users(driver, username, password, expected):
    print(f"\n👤 Testing user: {username}")
    driver.get(BASE_URL)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "user-name")))

    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)

    if expected == "pass":
        # Should land on inventory page
        if "inventory" in driver.current_url:
            print(f"✅ {username} — Login PASSED as expected!")
            results.append(f"✅ {username} — PASSED")
        else:
            print(f"❌ {username} — Should have passed but FAILED!")
            results.append(f"❌ {username} — FAILED (expected pass)")
            pytest.fail(f"{username} should have logged in but didn't")

    elif expected == "fail":
        # Should show error message
        try:
            error = driver.find_element(By.CLASS_NAME, "error-message-container")
            if error.is_displayed():
                print(f"✅ {username} — Blocked as expected!")
                results.append(f"✅ {username} — Blocked correctly")
        except:
            print(f"❌ {username} — Should have failed but PASSED!")
            results.append(f"❌ {username} — FAILED (expected block)")
            pytest.fail(f"{username} should have been blocked but wasn't")

# -----------------------------------------------
# FINAL — Send summary to Slack
# -----------------------------------------------
def pytest_sessionfinish(session, exitstatus):
    if not results:
        return
    total   = len(results)
    passed  = sum(1 for r in results if "PASSED" in r or "Blocked" in r)
    failed  = total - passed

    message = f"🤖 *Data-Driven Test Results — SauceDemo*\n\n"
    message += "\n".join(results)
    message += f"\n\n📊 Total: {total} | ✅ Passed: {passed} | ❌ Failed: {failed}"
    message += f"\n{'🎉 All tests passed!' if failed == 0 else '⚠️ Some tests failed!'}"

    send_to_slack(message)
    print("\n📨 Results sent to Slack!")
    print(f"\n📊 Total: {total} | ✅ Passed: {passed} | ❌ Failed: {failed}")
