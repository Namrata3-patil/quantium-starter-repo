import pytest
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from app import app  # Imports your Dash app instance

# 1. Background server fixture to spin up the Dash app
@pytest.fixture(scope="module", autouse=True)
def server():
    # Run the Dash server in a separate background thread so tests can interact with it
    thread = threading.Thread(target=lambda: app.run(debug=False, port=8050, use_reloader=False))
    thread.daemon = True
    thread.start()
    time.sleep(2)  # Give the server a couple of seconds to boot up smoothly
    yield

# 2. Browser fixture using standard headless Chrome
@pytest.fixture(scope="module")
def browser():
    options = Options()
    options.add_argument("--headless")  # Runs in the background without opening a visible window
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

# --- THE TESTS ---

# Test 1: Verify the Header is present and correct
def test_header_present(browser):
    browser.get("http://127.0.0.1:8050/")
    time.sleep(1)  # Let the page finish rendering
    
    header = browser.find_element(By.ID, "app-header")
    assert header is not None
    assert header.text == "Soul Foods Sales Visualizer"

# Test 2: Verify the Visualisation Graph is present
def test_visualization_present(browser):
    browser.get("http://127.0.0.1:8050/")
    time.sleep(1)
    
    graph = browser.find_element(By.ID, "sales-line-chart")
    assert graph is not None

# Test 3: Verify the Region Picker (Radio Items) is present
def test_region_picker_present(browser):
    browser.get("http://127.0.0.1:8050/")
    time.sleep(1)
    
    picker = browser.find_element(By.ID, "region-filter")
    assert picker is not None