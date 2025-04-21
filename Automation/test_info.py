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
    print("📍 Opening login page...")
    driver.get("http://127.0.0.1:5000/login")

    print("📍 Logging in...")
    driver.find_element(By.NAME, "username").send_keys("maggie")
    driver.find_element(By.NAME, "password").send_keys("12345")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()

    print("📍 Waiting for dashboard...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Information"))
    )

    print("📍 Opening Information page...")
    driver.find_element(By.LINK_TEXT, "Information").click()

    print("📍 Waiting for search input...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "query"))
    ).send_keys("The Signing of the U.S. Constitution (1787)")

    print("📍 Submitting search...")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]").click()

    print("📍 Waiting for search results...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "card-title"))
    )
    time.sleep(1)

    page_source = driver.page_source
    if "The Signing of the U.S. Constitution (1787)" in page_source:
        print("✅ Search successful! Result found.")
    else:
        print("❌ Search failed or result not found.")

except Exception as e:
    print(f"❌ Error during search automation: {e}")

finally:
    time.sleep(5)
    driver.quit()
