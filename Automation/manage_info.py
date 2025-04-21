from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Edge setup
options = Options()
options.add_argument('--start-maximized')
service = Service()
driver = webdriver.Edge(service=service, options=options)

try:
    print("📍 Opening admin login page...")
    driver.get("http://127.0.0.1:5000/login")
    print("📍 Logging in as admin...")
    driver.find_element(By.NAME, "username").send_keys("admin123")
    driver.find_element(By.NAME, "password").send_keys("adminpass")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()

    print("📍 Waiting for dashboard...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Manage Information"))
    )

    print("📍 Navigating to 'Manage Information'...")
    driver.find_element(By.LINK_TEXT, "Manage Information").click()

    print("📍 Waiting for table to load...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'table')]"))
    )

    print("📍 Verifying that information is displayed...")
    table = driver.find_element(By.XPATH, "//table[contains(@class, 'table')]")
    rows = table.find_elements(By.XPATH, ".//tbody//tr")
    if rows:
        print(f"✅ Found {len(rows)} pieces of information.")
    else:
        print("❌ No information found.")

    print("📍 Clicking 'Add New Information' button...")
    add_info_btn = driver.find_element(By.LINK_TEXT, "Add New Information")
    add_info_btn.click()

    print("📍 Filling in 'Add Information' form...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Add Information')]"))
    )

    driver.find_element(By.NAME, "title").send_keys("The Industrial Revolution")
    driver.find_element(By.NAME, "details").send_keys(
        "The Industrial Revolution began in the late 18th century and saw technological advances in machinery and factories."
    )

    print("📍 Submitting the form using the 'Add' button...")
    add_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Add')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)  # Ensure the button is in view
    time.sleep(1)
    add_btn.click()

    print("📍 Waiting for redirection and checking if information is added...")
    WebDriverWait(driver, 10).until(EC.url_contains("/admin/manage_information"))
    time.sleep(1)

    page_source = driver.page_source
    if "The Industrial Revolution" in page_source:
        print("✅ Information added successfully by admin!")
    else:
        print("❌ Information not found after submission.")

except Exception as e:
    print(f"❌ Error during admin information automation: {e}")
    print(driver.page_source)  # Print page source for debugging

finally:
    time.sleep(5)
    driver.quit()
