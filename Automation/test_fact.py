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
        EC.presence_of_element_located((By.LINK_TEXT, "Facts"))
    )

    print("📍 Opening Facts page...")
    driver.find_element(By.LINK_TEXT, "Facts").click()

    print("📍 Waiting for 'Add a Fact' button...")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Add a Fact"))
    ).click()

    print("📍 Filling in fact form...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "title"))
    ).send_keys("Invention of Internet")

    driver.find_element(By.NAME, "description").send_keys("The internet was born in 1983 with the TCP/IP protocol.")

    print("📍 Submitting the fact...")
    submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    time.sleep(1)
    submit_btn.click()

    print("📍 Waiting for redirection and checking if fact is added...")
    WebDriverWait(driver, 10).until(EC.url_contains("/facts"))
    time.sleep(1)

    page_source = driver.page_source
    if "Invention of Internet" in page_source:
        print("✅ Fact added successfully!")
    else:
        print("❌ Fact not found after submission.")

except Exception as e:
    print(f"❌ Error during facts automation: {e}")

finally:
    time.sleep(5)
    driver.quit()
