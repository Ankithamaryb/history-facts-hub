from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Edge driver
options = Options()
options.add_argument('--start-maximized')
service = Service()  # If needed, you can specify path here
driver = webdriver.Edge(service=service, options=options)

try:
    # ----------------- LOGIN -----------------
    print("📍 Opening login page...")
    driver.get("http://127.0.0.1:5000/login")

    print("📍 Logging in...")
    driver.find_element(By.NAME, "username").send_keys("maggie")
    driver.find_element(By.NAME, "password").send_keys("12345")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Facts"))
    )

    # ----------------- ADD A FACT -----------------
    print("📍 Navigating to Facts...")
    driver.find_element(By.LINK_TEXT, "Facts").click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Add a Fact"))
    ).click()

    print("📍 Adding a new fact...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "title"))
    ).send_keys("Invention of Internet")

    driver.find_element(By.NAME, "description").send_keys("The internet was born in 1983 with the TCP/IP protocol.")

    submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    submit_btn.click()

    WebDriverWait(driver, 10).until(EC.url_contains("/facts"))
    time.sleep(1)
    if "Invention of Internet" in driver.page_source:
        print("✅ Fact added successfully!")
    else:
        print("❌ Fact not found.")

    # ----------------- SEARCH INFORMATION -----------------
    print("📍 Navigating to Information page...")
    driver.find_element(By.LINK_TEXT, "Information").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "query"))
    ).send_keys("The Signing of the U.S. Constitution (1787)")

    driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "card-title"))
    )
    if "The Signing of the U.S. Constitution (1787)" in driver.page_source:
        print("✅ Search successful!")
    else:
        print("❌ Search result not found.")

    # ----------------- TAKE QUIZ -----------------
    print("📍 Opening quiz page...")
    driver.find_element(By.LINK_TEXT, "Quiz").click()

    print("📍 Starting quiz...")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Take Quiz"))
    ).click()

    print("📍 Selecting answers...")
    # Wait for the quiz form to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "form-check-input"))
    )

    # Select first option for each question
    radio_buttons = driver.find_elements(By.CSS_SELECTOR, ".card .form-check-input:first-child")
    for idx, btn in enumerate(radio_buttons):
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            time.sleep(0.2)
            btn.click()
        except Exception as e:
            print(f"⚠️ Could not click option for question {idx + 1}: {e}")

    print("📍 Submitting quiz...")
    submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit Quiz')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    time.sleep(1)
    submit_btn.click()

    print("✅ Quiz submitted successfully!")

except Exception as e:
    print(f"❌ Error during quiz automation: {e}")
finally:
    time.sleep(5)
    driver.quit()
